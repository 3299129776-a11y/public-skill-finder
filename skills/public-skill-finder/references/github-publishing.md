# GitHub Publishing

Use this reference when preparing the skill for a public GitHub repository.

## Repository Shape

The repository can contain the skill at its root:

```text
public-skill-finder/
  SKILL.md
  agents/
    openai.yaml
  scripts/
    find_public_skills.py
  references/
    search-and-evaluation.md
    github-publishing.md
```

Keep the skill package focused. Avoid adding extra documentation files inside the skill unless the hosting platform requires them.

## Install From GitHub

After publishing to GitHub, install with:

```bash
npx -y skills@latest add owner/repo -g -y
```

If the repository contains multiple skills, install this one explicitly:

```bash
npx -y skills@latest add owner/repo --skill public-skill-finder -g -y
```

If the repository stores the skill in a subdirectory, confirm the installer supports that repository layout before publishing.

## Public Repository Requirements

Do not add:

- Hardcoded private registry configuration
- Organization-specific authentication flows
- Internal package mirrors
- Telemetry scripts
- Required API keys

The helper script may support internal registry searches, but a public GitHub repository should leave registry/auth details to the user's local `skills@latest` configuration.

## Release Checklist

Before publishing:

1. Run `quick_validate.py` on the skill folder.
2. Run the helper script with `--no-cli`.
3. Run one live search if npm and network are available.
4. Confirm no company-specific registry or credential is hardcoded.
5. Confirm `SKILL.md` frontmatter contains only `name` and `description`.
