# Public Skill Finder

`public-skill-finder` helps users discover and install publicly available agent skills from external/open-source registries.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## How to Help Users Find Skills

### Step 1: Extract Search Keywords (CRITICAL)

The public skill registry search supports traditional keyword search. It does not understand natural language or semantic queries. Before running the find command, convert the user's intent into concise, space-separated keywords.

Keyword extraction rules:

1. Remove filler words (how, do, I, can, you, help, me, want, need, etc.)
2. Keep domain-specific terms (react, go, kafka, docker, kubernetes, etc.)
3. Keep action verbs that describe the task (deploy, test, monitor, review, lint, etc.)
4. Use lowercase
5. Aim for 2-4 keywords for best results

## What It Does

- Converts natural-language requests into concise registry search keywords.
- Searches public skills through `skills@latest`.
- Cleans CLI output, deduplicates results, and renders Markdown or JSON summaries.
- Guides agents to verify a candidate skill before recommending it.

## Install

Install this skill from the repository:

```bash
npx -y skills@latest add 3299129776-a11y/public-skill-finder --skill public-skill-finder -g -y --full-depth
```

## Usage

Ask Codex:

```text
Use $public-skill-finder to find a skill for resume generation.
```

Or run the helper script directly from the skill directory:

```bash
python scripts/find_public_skills.py "resume generator" --extra-query "cv resume" --limit 5
python scripts/find_public_skills.py "social media analytics" --format json --limit 3
```

Manual CLI equivalent:

```bash
npx -y skills@latest find resume generator --source external -y
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

This repository is scoped to public/open-source skill discovery. It does not include private registry configuration, organization-specific authentication flows, package mirrors, or telemetry hooks.
