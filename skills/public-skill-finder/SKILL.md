---
name: public-skill-finder
description: Helps users discover and install publicly available agent skills from external/open-source registries when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. Use when the user is looking for functionality that might exist as an installable skill.
---

# Public Skill Finder

Find publicly available installable agent skills that match the user's described task.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## Workflow

1. Extract search keywords.
   - The public skill registry search supports traditional keyword search. It does not understand natural language or semantic queries.
   - Before running the find command, convert the user's intent into concise, space-separated keywords.
   - Remove filler words (how, do, I, can, you, help, me, want, need, etc.).
   - Keep domain-specific terms (react, go, kafka, docker, kubernetes, etc.).
   - Keep action verbs that describe the task (deploy, test, monitor, review, lint, etc.).
   - Use lowercase.
   - Aim for 2-4 keywords for best results.
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
   - Prefer higher install counts, trusted maintainers, clear `SKILL.md` content, and direct task match.
5. Present concise recommendations with:
   - Skill package name
   - Source link when available
   - Why it fits
   - Caveats such as API keys, paid services, auth requirements, or low adoption
   - Install command

## Manual Fallback

If the helper script cannot run, call the skills CLI directly:

```bash
npx -y skills@latest find resume generator --source external -y
```

For package inspection, open the `skills.sh` or public GitHub link when available. Do not recommend a skill based only on its name.

## Output Template

```markdown
I found a few public skills that may fit:

**[Public]** `owner/repo@skill-name`
Source: https://skills.sh/owner/repo/skill-name
Best for: [specific use case]
Caveats: [none / needs API key / low adoption / verify docs]
Install:
`npx -y skills@latest add "owner/repo@skill-name" -g -y`
```

When no relevant skills are found, say what searches were tried, suggest alternate keywords, and offer to help directly or create a new skill.

## Publishing Reference

Read `references/github-publishing.md` when the user asks how to publish, package, or install this skill from a GitHub repository.
