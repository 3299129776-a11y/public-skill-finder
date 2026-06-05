# Search And Evaluation

Use this reference when search results need quality judgment before recommendation.

## Keyword Strategy

Public skill search is keyword-based, not semantic. Turn the user's intent into short queries:

| User intent | Query examples |
| --- | --- |
| Generate resumes | `resume generator`, `cv resume`, `job application` |
| Analyze social traffic | `social media analytics`, `traffic analysis`, `content analytics` |
| Test web apps | `playwright testing`, `e2e test`, `webapp testing` |
| Work with documents | `docx`, `pdf extraction`, `document processing` |

Run two or three distinct queries when the first result set is weak.

## Quality Signals

Prefer candidates with:

- Clear `skills.sh` page or public GitHub repository.
- Higher install counts than nearby alternatives.
- A `SKILL.md` description that directly matches the task.
- Maintainer reputation, such as official organizations, known projects, or focused skill collections.
- Concrete workflows, scripts, references, or assets that support the task.

Be cautious when:

- The name matches but the `SKILL.md` solves a different problem.
- Install count is very low.
- The skill requires a paid API, private account, or opaque external service.
- The repository is unavailable or has no readable skill files.
- The result title contains spaces or unusual characters; quote install commands and verify the package identifier.

## Verification Steps

1. Open the `skills.sh` link from the result.
2. If needed, inspect the linked public GitHub `SKILL.md`.
3. Confirm the trigger description and workflow fit the user's task.
4. Check whether dependencies or API keys are required.
5. Recommend only the best few options, not every search hit.

## Recommendation Format

For each candidate, include:

- **[External]** label
- Package identifier
- Source URL
- Best-fit use case
- Caveats
- Install command

Example:

```markdown
**[External]** `owner/repo@resume-generator`
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
