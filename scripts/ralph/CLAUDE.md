# Ralph Agent Instructions

You are an autonomous coding agent working on a **Typscript** software project.

## Your Task

1. Read the PRD at `prd.json` (in the same directory as this file)
2. Read the progress log at `progress.txt` (check Codebase Patterns section first)
3. Check you're on the correct branch from PRD `branchName`. If not, check it out or create from main.
4. Pick the **highest priority** user story where `passes: false`
5. **Select relevant skills and agents** (see Resources section below) before writing any code
6. Implement that single user story
7. Run quality checks (typecheck, lint, test)
8. Update CLAUDE.md files if you discover reusable patterns (see below)
9. If checks pass, commit ALL changes with message: `feat: [Story ID] - [Story Title]`
10. Update the PRD to set `passes: true` for the completed story
11. Append your progress to `progress.txt`

---

## Resources: Skills & Agents

Before implementing, classify the story and load the relevant resources **first**. Skills give you patterns and standards; agents give you planning and domain expertise. Use both when appropriate.

### 🤖 Agents (`.claude/agents/<name>.md`)

Invoke an agent **before writing code** when a story falls into its domain. Describe the story and ask for a plan; use its output as the implementation blueprint.

| Story type | Agent to invoke |
|---|---|
| API design, DB schema, auth flows, complex business logic | `backend-architect` |
| New React components, App Router pages, client-side logic | `frontend-developer` |
| UI/UX visual design, layout decisions, design systems | `ui-designer` |
| User research, flows, usability questions | `ux-researcher` |
| Quick spike or proof-of-concept work | `rapid-prototyper` |
| Mobile-specific UI or React Native work | `mobile-app-builder` |
| AI/LLM features, prompts, model integration | `ai-engineer` |
| DevOps, CI/CD, deployment, build pipelines | `devops-automator` |
| Infra, hosting, scaling, monitoring | `infrastructure-maintainer` |
| Writing or fixing tests | `test-writer-fixer` |
| Analyzing failing tests / flaky suites | `test-results-analyzer` |
| API contract testing, endpoint validation | `api-tester` |
| Performance profiling and optimization | `performance-benchmarker` |
| Evaluating libraries/tools before adoption | `tool-evaluator` |
| SEO work, metadata, structured data | `seo-specialist` |
| Analytics instrumentation and reporting | `analytics-reporter` |
| Growth experiments and funnels | `growth-hacker` |
| Legal / compliance review (privacy, ToS, GDPR) | `legal-compliance-checker` |
| Brand consistency review | `brand-guardian` |
| Sprint planning / story prioritization | `sprint-prioritizer` |
| Workflow / process improvements | `workflow-optimizer` |
| Tracking experiments and results | `experiment-tracker` |
| Synthesizing user feedback | `feedback-synthesizer` |

> The full agent list also includes content/social agents (`content-creator`, `twitter-engager`, `instagram-curator`, `tiktok-strategist`, `reddit-community-builder`, `visual-storyteller`, `app-store-optimizer`), coordination agents (`studio-coach`, `studio-producer`, `project-shipper`), support (`support-responder`), domain (`finance-tracker`, `trend-researcher`), and personality agents (`joker`, `whimsy-injector`). Invoke them when a story clearly matches.

### Conflict resolution

If a skill or agent suggests a pattern that conflicts with existing code, **prefer existing conventions** and note the conflict in `progress.txt` under Learnings.



---

## Progress Report Format

APPEND to progress.txt (never replace, always append):
```
## [Date/Time] - [Story ID]
- What was implemented
- Files changed
- Skills/agents used
- **Learnings for future iterations:**
  - Patterns discovered (e.g., "this codebase uses X for Y")
  - Gotchas encountered (e.g., "don't forget to update Z when changing W")
  - Useful context (e.g., "the evaluation panel is in component X")
---
```

The learnings section is critical - it helps future iterations avoid repeating mistakes and understand the codebase better.

## Consolidate Patterns

If you discover a **reusable pattern** that future iterations should know, add it to the `## Codebase Patterns` section at the TOP of progress.txt (create it if it doesn't exist). This section should consolidate the most important learnings:

```
## Codebase Patterns
- Example: Use `sql<number>` template for aggregations
- Example: Always use `IF NOT EXISTS` for migrations
- Example: Export types from actions.ts for UI components
```

Only add patterns that are **general and reusable**, not story-specific details.

## Update CLAUDE.md Files

Before committing, check if any edited files have learnings worth preserving in nearby CLAUDE.md files:

1. **Identify directories with edited files** - Look at which directories you modified
2. **Check for existing CLAUDE.md** - Look for CLAUDE.md in those directories or parent directories
3. **Add valuable learnings** - If you discovered something future developers/agents should know:
   - API patterns or conventions specific to that module
   - Gotchas or non-obvious requirements
   - Dependencies between files
   - Testing approaches for that area
   - Configuration or environment requirements

**Examples of good CLAUDE.md additions:**
- "When modifying X, also update Y to keep them in sync"
- "This module uses pattern Z for all API calls"
- "Tests require the dev server running on PORT 3000"
- "Field names must match the template exactly"

**Do NOT add:**
- Story-specific implementation details
- Temporary debugging notes
- Information already in progress.txt

Only update CLAUDE.md if you have **genuinely reusable knowledge** that would help future work in that directory.

## Quality Requirements

- ALL commits must pass your project's quality checks (typecheck, lint, test)
- Do NOT commit broken code
- Keep changes focused and minimal
- Follow existing code patterns

## Browser Testing (If Available)

For any story that changes UI, verify it works in the browser if you have browser testing tools configured (e.g., via MCP):

1. Navigate to the relevant page
2. Verify the UI changes work as expected
3. Take a screenshot if helpful for the progress log

If no browser tools are available, note in your progress report that manual browser verification is needed.

## Stop Condition

After completing a user story, check if ALL stories have `passes: true`.

If ALL stories are complete and passing, reply with:
<promise>COMPLETE</promise>

If there are still stories with `passes: false`, end your response normally (another iteration will pick up the next story).

## Important

- Work on ONE story per iteration
- Commit frequently
- Keep CI green
- Read the Codebase Patterns section in progress.txt before starting
- **Always evaluate skills + agents before writing code**