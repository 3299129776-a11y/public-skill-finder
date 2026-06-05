# Skill Finder

`public-skill-finder` is a Codex skill for discovering and installing agent skills from both internal company registries and external open-source registries.

It is designed for requests like:

- "How do I make my React app faster?"
- "Find a skill for resume generation"
- "Is there a skill that can analyze social media traffic?"
- "Recommend an installable skill for PDF extraction"
- "Search internal and external skill registries and compare the best options"

## What It Does

- Converts natural-language requests into concise registry search keywords.
- Searches both internal and external registries by default through `skills@latest`.
- Supports source filtering with `--source internal` or `--source external`.
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
python scripts/find_public_skills.py "social media analytics" --source external --format json --limit 3
python scripts/find_public_skills.py "deploy cloud" --source internal --limit 5
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

This public repository does not hardcode any specific company's private registry, SSO, npm mirror, or telemetry hook. Internal registry searches depend on the user's local `skills@latest` setup and authentication.
