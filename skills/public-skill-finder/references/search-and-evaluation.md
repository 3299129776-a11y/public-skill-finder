# Search And Evaluation

Use this reference when search results need quality judgment before recommendation.

## Keyword Strategy

Skill registry search is keyword-based, not semantic. Turn the user's intent into short queries:

| User intent | Query examples |
| --- | --- |
| Generate resumes | `resume generator`, `cv resume`, `job application` |
| Analyze social traffic | `social media analytics`, `traffic analysis`, `content analytics` |
| Test web apps | `playwright testing`, `e2e test`, `webapp testing` |
| Work with documents | `docx`, `pdf extraction`, `document processing` |
| Deploy internal service | `deploy cloud`, `kubernetes deploy`, `ci cd` |

Run two or three distinct queries when the first result set is weak.

## Quality Signals

Prefer candidates with:

- Clear registry page, `skills.sh` page, or public GitHub repository.
- Higher install counts than nearby alternatives.
- A `SKILL.md` description that directly matches the task.
- Trusted maintainers, such as internal platform teams, official organizations, known projects, or focused skill collections.
- Concrete workflows, scripts, references, or assets that support the task.

Be cautious when:

- The name matches but the `SKILL.md` solves a different problem.
- Install count is very low.
- The skill requires a paid API, private account, or opaque external service.
- The repository or registry page is unavailable.
- The result title contains spaces or unusual characters; quote install commands and verify the package identifier.
- Internal results require authentication that the current environment does not have.

## Verification Steps

1. Confirm whether the result is internal or external.
2. Open the `skills.sh`, GitHub, or internal registry link when available.
3. Confirm the trigger description and workflow fit the user's task.
4. Check whether dependencies, API keys, or internal auth are required.
5. Recommend only the best few options, not every search hit.

## Recommendation Format

For each candidate, include:

- **[Internal]** or **[External]** label
- Package identifier
- Source URL when available
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
- Say whether internal, external, or both sources were searched.
- Suggest broader or alternate keywords.
- Offer to help perform the task directly.
- Offer to create a new skill if the workflow is reusable.
