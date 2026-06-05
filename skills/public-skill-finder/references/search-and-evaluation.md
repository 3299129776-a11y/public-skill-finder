# Search And Evaluation

Use this reference when search results need quality judgment before recommendation.

## Keyword Strategy

The public skill registry search supports traditional keyword search. It does not understand natural language or semantic queries. Before running the find command, convert the user's intent into concise, space-separated keywords.

Keyword extraction rules:

1. Remove filler words (how, do, I, can, you, help, me, want, need, etc.)
2. Keep domain-specific terms (react, go, kafka, docker, kubernetes, etc.)
3. Keep action verbs that describe the task (deploy, test, monitor, review, lint, etc.)
4. Use lowercase
5. Aim for 2-4 keywords for best results

Examples:

| User intent | Query examples |
| --- | --- |
| Generate resumes | `resume generator`, `cv resume`, `job application` |
| Analyze social traffic | `social media analytics`, `traffic analysis`, `content analytics` |
| Test web apps | `playwright testing`, `e2e test`, `webapp testing` |
| Work with documents | `docx`, `pdf extraction`, `document processing` |
| Deploy a service | `deploy cloud`, `kubernetes deploy`, `ci cd` |

Run two or three distinct queries when the first result set is weak.

## Quality Signals

Prefer candidates with:

- Clear `skills.sh` page or public GitHub repository.
- Higher install counts than nearby alternatives.
- A `SKILL.md` description that directly matches the task.
- Trusted maintainers, such as official organizations, known projects, or focused skill collections.
- Concrete workflows, scripts, references, or assets that support the task.

Be cautious when:

- The name matches but the `SKILL.md` solves a different problem.
- Install count is very low.
- The skill requires a paid API, private account, or opaque external service.
- The repository or registry page is unavailable.
- The result title contains spaces or unusual characters; quote install commands and verify the package identifier.

## Verification Steps

1. Open the `skills.sh` or GitHub link when available.
2. Confirm the trigger description and workflow fit the user's task.
3. Check whether dependencies, API keys, accounts, or paid services are required.
4. Recommend only the best few options, not every search hit.

## Recommendation Format

For each candidate, include:

- Package identifier
- Source URL when available
- Best-fit use case
- Caveats
- Install command

Example:

```markdown
**[Public]** `owner/repo@resume-generator`
Source: https://skills.sh/owner/repo/resume-generator
Best for: Creating ATS-friendly resumes from a job description.
Caveats: Verify the linked `SKILL.md` before using it for sensitive personal data.
Install: `npx -y skills@latest add "owner/repo@resume-generator" -g -y`
```

## No Good Match

If no candidate is relevant:

- State the exact queries tried.
- Suggest broader or alternate keywords.
- Offer to help perform the task directly.
- Offer to create a new skill if the workflow is reusable.
