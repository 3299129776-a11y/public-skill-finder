#!/usr/bin/env python3
"""Find installable skills from internal and external skills registries."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from typing import Any


ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
INSTALL_RE = re.compile(r"^(?P<package>.+?)\s+(?P<count>\d+(?:\.\d+)?[KMB]?)\s+installs?$", re.I)
URL_RE = re.compile(r"https://skills\.sh/\S+")


def strip_ansi(text: str) -> str:
    """Remove terminal ANSI escape sequences from CLI output."""
    return ANSI_RE.sub("", text)


def parse_install_count(value: str) -> int:
    """Convert values like 180, 1.2K, or 2M into integers."""
    suffixes = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}
    value = value.strip().upper()
    suffix = value[-1]
    if suffix in suffixes:
        return int(float(value[:-1]) * suffixes[suffix])
    return int(float(value))


def parse_cli_output(raw_output: str, query: str, source_hint: str = "both") -> list[dict[str, Any]]:
    """Extract skill candidates from `skills find` output."""
    text = strip_ansi(raw_output)
    candidates: list[dict[str, Any]] = []
    last_candidate: dict[str, Any] | None = None
    has_section_headers = any(line.strip().endswith("SKILLS") for line in text.splitlines())
    current_source = source_hint if source_hint in {"internal", "external"} else "external"
    in_result_section = not has_section_headers

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "INTERNAL SKILLS":
            current_source = "internal"
            in_result_section = True
            last_candidate = None
            continue
        if line == "EXTERNAL SKILLS":
            current_source = "external"
            in_result_section = True
            last_candidate = None
            continue
        if line.endswith("SKILLS"):
            in_result_section = False
            last_candidate = None
            continue
        if not in_result_section:
            continue

        url_match = URL_RE.search(line)
        if url_match and last_candidate is not None:
            last_candidate["url"] = url_match.group(0)
            continue

        install_match = INSTALL_RE.match(line)
        if not install_match:
            continue

        package = install_match.group("package").strip()
        candidate = {
            "package": package,
            "name": package.split("@", 1)[-1],
            "repository": package.split("@", 1)[0] if "@" in package else "",
            "installs": parse_install_count(install_match.group("count")),
            "url": "",
            "source": current_source,
            "query": query,
        }
        candidates.append(candidate)
        last_candidate = candidate

    return candidates


def deduplicate(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the first candidate for each package while preserving order."""
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for candidate in candidates:
        key = candidate["package"].lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)
    return deduped


def build_skills_find_command(query: str, source: str = "both") -> list[str]:
    """Build a platform-safe skills CLI command."""
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if npx is None:
        raise FileNotFoundError("npx")
    command = [
        npx,
        "-y",
        "skills@latest",
        "find",
        *query.split(),
    ]
    if source in {"internal", "external"}:
        command.extend(["--source", source])
    command.append("-y")
    return command


def run_skills_find(query: str, timeout: int, source: str = "both") -> tuple[str, str | None]:
    """Run `skills find` against selected registries."""
    try:
        command = build_skills_find_command(query, source=source)
    except FileNotFoundError:
        return "", "`npx` was not found. Install Node.js/npm or run the search manually."
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "", f"Search timed out after {timeout} seconds: {query}"

    combined_output = "\n".join(part for part in [result.stdout, result.stderr] if part)
    if result.returncode != 0:
        return combined_output, f"Search command exited with code {result.returncode}: {query}"
    return combined_output, None


def build_queries(primary_queries: list[str], extra_queries: list[str] | None) -> list[str]:
    """Normalize and deduplicate query strings."""
    queries: list[str] = []
    for query in [*primary_queries, *(extra_queries or [])]:
        cleaned = " ".join(query.lower().split())
        if cleaned and cleaned not in queries:
            queries.append(cleaned)
    return queries


def render_markdown(
    candidates: list[dict[str, Any]],
    queries: list[str],
    errors: list[str],
    limit: int,
) -> str:
    """Render search results for direct use in chat."""
    lines = [
        "# Skill Search Results",
        "",
        f"Queries: {', '.join(f'`{query}`' for query in queries)}",
        "",
    ]

    if errors:
        lines.append("## Notes")
        for error in errors:
            lines.append(f"- {error}")
        lines.append("")

    if not candidates:
        lines.extend(
            [
                "No skill candidates were found.",
                "",
                "Try broader keywords, alternate spellings, or a domain term plus an action verb.",
            ]
        )
        return "\n".join(lines)

    lines.append("## Candidates")
    for index, candidate in enumerate(candidates[:limit], start=1):
        package = candidate["package"]
        install_command = f'npx -y skills@latest add "{package}" -g -y'
        lines.extend(
            [
                f"{index}. **[{candidate['source'].title()}]** `{package}`",
                f"   - Installs: {candidate['installs']}",
                f"   - Matched query: `{candidate['query']}`",
                f"   - Source: {candidate['url'] or 'No skills.sh URL found in CLI output'}",
                f"   - Install: `{install_command}`",
            ]
        )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search internal and external agent skill registries.",
    )
    parser.add_argument("queries", nargs="+", help="Primary search query or queries.")
    parser.add_argument(
        "--extra-query",
        action="append",
        default=[],
        help="Additional query to run. Can be provided multiple times.",
    )
    parser.add_argument("--limit", type=int, default=6, help="Maximum candidates to output.")
    parser.add_argument(
        "--source",
        choices=["both", "internal", "external"],
        default="both",
        help="Registry source to search.",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Per-query command timeout in seconds.",
    )
    parser.add_argument(
        "--no-cli",
        action="store_true",
        help="Skip npx execution; useful for smoke-testing argument parsing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    queries = build_queries(args.queries, args.extra_query)
    errors: list[str] = []
    candidates: list[dict[str, Any]] = []

    if args.no_cli:
        errors.append("CLI execution skipped because `--no-cli` was provided.")
    else:
        for query in queries:
            output, error = run_skills_find(query, timeout=args.timeout, source=args.source)
            if error:
                errors.append(error)
            candidates.extend(parse_cli_output(output, query=query, source_hint=args.source))

    candidates = deduplicate(candidates)
    candidates.sort(key=lambda candidate: candidate["installs"], reverse=True)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "queries": queries,
                    "errors": errors,
                    "candidates": candidates[: args.limit],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(render_markdown(candidates, queries, errors, args.limit))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
