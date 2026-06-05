---
name: public-skill-finder
description: Helps users discover and install agent skills from both internal (company) and external (open-source) registries when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
---

# Skill Finder

Find installable agent skills from internal company registries and external open-source registries, then recommend only candidates that look relevant and usable.

## Boundaries

- Search both internal and external sources by default.
- Use `--source internal` or `--source external` only when the user asks to limit scope.
- Do not hardcode one company's private registry, SSO, npm mirror, or telemetry hook in this public GitHub skill.
- Internal registry results may require the user's local `skills@latest` authentication and registry configuration.
- Do not install a skill unless the user explicitly asks.
- Label every recommendation as **[Internal]** or **[External]**.

## Workflow

1. Convert the user's request into 2-4 lowercase keywords.
   - Remove filler words.
   - Keep domain nouns and action verbs.
   - Prefer English keywords first, then try local-language terms if relevant.
2. Run the helper script from this skill directory:

```bash
python scripts/find_public_skills.py "resume generator" --extra-query "cv resume" --limit 6
```

3. To search only one side:

```bash
python scripts/find_public_skills.py "resume generator" --source external
python scripts/find_public_skills.py "deploy cloud" --source internal
```

4. If results are weak, run alternate queries:
   - Use synonyms: `resume`, `cv`, `career`, `job application`.
   - Pair domain + action: `react testing`, `seo audit`, `pdf extraction`.
   - Try narrower or broader terms.
5. Verify candidates before recommending them.
   - Read `references/search-and-evaluation.md` when judging quality or relevance.
   - Prefer higher install counts, trusted maintainers, clear `SKILL.md` content, and direct task match.
6. Present concise recommendations with:
   - Source label
   - Skill package name
   - Source link when available
   - Why it fits
   - Caveats such as API keys, paid services, auth requirements, or low adoption
   - Install command

## Manual Fallback

If the helper script cannot run, call the skills CLI directly:

```bash
npx -y skills@latest find resume generator -y
npx -y skills@latest find resume generator --source external -y
npx -y skills@latest find deploy cloud --source internal -y
```

For package inspection, open the `skills.sh` or public GitHub link when available. For internal results, inspect the internal registry page or package docs if the user's environment exposes them. Do not recommend a skill based only on its name.

## Output Template

```markdown
I found a few skills that may fit:

**[External]** `owner/repo@skill-name`
Source: https://skills.sh/owner/repo/skill-name
Best for: [specific use case]
Caveats: [none / needs API key / low adoption / verify docs]
Install:
`npx -y skills@latest add "owner/repo@skill-name" -g -y`

**[Internal]** `team-or-registry@skill-name`
Source: [internal registry page if available]
Best for: [specific use case]
Caveats: Requires internal registry access/authentication.
Install:
`npx -y skills@latest add "team-or-registry@skill-name" -g -y`
```

When no relevant skills are found, say what searches were tried, suggest alternate keywords, and offer to help directly or create a new skill.

## Publishing Reference

Read `references/github-publishing.md` when the user asks how to publish, package, or install this skill from a GitHub repository.
