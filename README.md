# Public Skill Finder

`public-skill-finder` is a Codex skill for discovering publicly available agent skills from GitHub-backed sources such as `skills.sh` and the external `skills@latest` registry.

It is designed for requests like:

- "Find a public skill for resume generation"
- "Is there a GitHub skill for social media analytics?"
- "Recommend an installable skill for PDF extraction"
- "Search public agent skills and compare the best options"

## What It Does

- Converts natural-language requests into concise public registry search keywords.
- Searches only public sources; no private registry, company SSO, or internal npm mirror is required.
- Uses a Python helper to run `npx -y skills@latest find ... --source external -y`.
- Cleans CLI output, deduplicates results, and renders Markdown or JSON summaries.
- Guides agents to verify a candidate skill before recommending it.

## Install

Install this skill from the repository:

```bash
npx -y skills@latest add OWNER/public-skill-finder --skill public-skill-finder -g -y --full-depth
```

Replace `OWNER` with the GitHub username or organization that owns this repository.

## Usage

Ask Codex:

```text
Use $public-skill-finder to find a public skill for resume generation.
```

Or run the helper script directly from the skill directory:

```bash
python scripts/find_public_skills.py "resume generator" --extra-query "cv resume" --limit 5
python scripts/find_public_skills.py "social media analytics" --format json --limit 3
```

## Repository Layout

```text
skills/
  public-skill-finder/
    SKILL.md
    agents/
      openai.yaml
    scripts/
      find_public_skills.py
    references/
      github-publishing.md
      search-and-evaluation.md
```

## Notes

This project intentionally avoids private registries, telemetry hooks, internal authentication, and required API keys. It only helps discover public skill packages and does not install anything unless the user explicitly asks.
