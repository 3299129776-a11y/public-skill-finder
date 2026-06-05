---
name: public-skill-finder
description: Use when users want to find, compare, verify, recommend, or install publicly available agent skills from GitHub-backed sources such as skills.sh or the external skills registry. Use for requests like "find a skill for X", "is there a public skill that can...", "look for GitHub skills", or "recommend a skill package".
---

# Public Skill Finder

Find public agent skills from GitHub-backed sources and recommend only candidates that look relevant and installable.

## Boundaries

- Search only public sources: `skills.sh`, the external `skills@latest` registry, and public GitHub repositories linked by those results.
- Do not use private registries, company npm mirrors, internal auth, SSO, or telemetry hooks.
- Do not install a skill unless the user explicitly asks.
- Label every recommendation as **[External]**.

## Workflow

1. Convert the user's request into 2-4 lowercase keywords.
   - Remove filler words.
   - Keep domain nouns and action verbs.
   - Prefer English keywords because public registry search is keyword-based.
2. Run the helper script from this skill directory:

```bash
python scripts/find_public_skills.py "resume generator" --extra-query "cv resume" --limit 6
```

3. If results are weak, run alternate queries:
   - Use synonyms: `resume`, `cv`, `career`, `job application`.
   - Pair domain + action: `react testing`, `seo audit`, `pdf extraction`.
   - Try narrower or broader terms.
4. Verify candidates before recommending them.
   - Read `references/search-and-evaluation.md` when judging quality or relevance.
   - Prefer higher install counts, reputable maintainers, clear `SKILL.md` content, and direct task match.
5. Present concise recommendations with:
   - Skill package name
   - Source link
   - Why it fits
   - Caveats such as API keys, paid services, or low adoption
   - Install command

## Manual Fallback

If the helper script cannot run, use the public external registry directly:

```bash
npx -y skills@latest find resume generator --source external -y
```

For package inspection, prefer public GitHub and `skills.sh` links from the result. Do not recommend a skill based only on its name.

## Output Template

```markdown
I found a few public skills that may fit:

**[External]** `owner/repo@skill-name`
Source: https://skills.sh/owner/repo/skill-name
Best for: [specific use case]
Caveats: [none / needs API key / low adoption / verify docs]
Install:
`npx -y skills@latest add "owner/repo@skill-name" -g -y`
```

When no relevant skills are found, say what searches were tried, suggest alternate keywords, and offer to help directly or create a new skill.

## Publishing Reference

Read `references/github-publishing.md` when the user asks how to publish, package, or install this skill from a GitHub repository.
