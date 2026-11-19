# Reverse engineering a UC spec from code

Use this when no user stories are provided, or the user points at a codebase and asks for documentation. The goal is a UC spec a business reader can verify, written from what the code actually does.

## 1. Find the code and fix the scope

- Look in the places the code is likely to be: `/mnt/user-data/uploads`, the working directory, or a repository the user names (cloning from github.com is allowed in this environment). If you cannot find it, ask for the location in one short question.
- A whole system is too large to document in one pass. If the user named a feature, module, route or screen, start there. If they did not, list the candidate features you found (grouped by module) and ask which to cover, or propose a sensible first batch.
- Do not read everything. Search first (routes, controllers, handlers, button/click handlers, scheduled jobs, message consumers), then read only the files on the traced path.

## 2. Find entry points, then trace each one

Each entry point that represents a user goal is a UC candidate. Typical entry points:

| Kind | Where to look |
|---|---|
| Web/API | Route tables, controllers, handlers, `@GetMapping`/`@PostMapping`, `app.get/post`, minimal API maps, view actions |
| UI | Click/submit handlers, form actions, command bindings, navigation calls |
| Background | Schedulers, cron jobs, queue/event consumers, webhooks |
| Batch/integration | Import/export jobs, external API clients |

Trace each one in this order and take notes as you go: **entry → authorization → input validation → business logic → persistence → side effects (email, events, audit, calls out) → response or navigation**.

## 3. Map code to template

| Template element | Source in code |
|---|---|
| Actor | Roles and permissions on the entry point (`[Authorize(Roles=...)]`, guards, policies, permission checks). No auth = ask or `<TBD>`. A scheduler or consumer = "System" (name the triggering system if external). |
| Trigger | The route, button handler or event that starts it, plus the screen or caller. |
| Pre-condition | Guards and early returns: login required, record must exist, record must be in a given status, feature flag on. |
| Post-condition | What the success path persists or emits: records created or changed, status set, notification sent. |
| Business Rules | Conditionals, validators, constants and enums, status transitions, calculations, ID/number generators, defaults, query filters and sorting, configuration values. |
| Alternative flows | Valid branches that reach the same goal: optional paths, "save as draft", confirm/decline, different user types. |
| Exception flows | Validation failures, `throw`/error returns, catch blocks, not-found and forbidden responses, transaction rollbacks. |
| Messages | Resource/i18n files, constants, toast and error strings. Use the message text; reference the message key as the source. |
| Common rules (CBR) | Shared helpers invoked in many places: audit logging, permission checks, notification utilities. Reference, do not copy. |

## 4. Write what the code does, in business language

- Describe observed behavior, not what you think it should do. If the code and common sense disagree, the spec follows the code and the discrepancy is reported.
- Translate technical terms into the language of the business. "Insert row into `case_tbl` with `status=2`" becomes "Create a new Case and update [Status] to "Assigned"". Use the label the user sees on screen for a field; use the column or property name only when there is no label.
- Keep implementation out of BRs: no SQL, class names, framework terms. Keep **values** in: formats, limits, thresholds, statuses, durations, because those are the rules.
- Resolve enums and magic numbers to meaning where the code or a lookup table says what they mean. If you cannot tell what `3` means, write `<TBD>` and say so.
- Message codes: use the text from the code. Use the team's catalog code if the user supplies one; otherwise `IEM <TBD>` or `CFD <TBD>` with the text. Never invent a code number.

## 5. Distinguish fact from inference

Every statement is one of two kinds. Keep them apart so reviewers know where to push:
- **Observed:** read directly in code. Write it plainly.
- **Inferred:** a purpose you deduced (why a rule exists, what a status means to the business). Write it as `<TBD: inferred - <what you think>>` or ask in the reply.

Report as open items, never silently fix or hide:
- Likely defects (missing validation, unreachable branches, off-by-one limits, inconsistent rules between screens).
- Dead code, commented-out features, `TODO`/`FIXME` notes that change behavior.
- Hard-coded values that look like they should be configurable.
- Behavior that depends on data or config you could not see (feature flags, DB lookup contents, environment settings).

## 6. Source traceability appendix

For reverse-engineered documents, append a short table at the end of the .md so a reviewer or developer can verify each rule:

```markdown
## Appendix: Source Traceability

| Item | Source |
|---|---|
| UC 1 trigger | `src/web/CasesController.cs` - `Create()` |
| BR 3 (assignment, SLA) | `src/services/CaseService.cs` - `Submit()`, lines 88-142 |
| IEM <TBD> text | `Resources/Messages.resx` key `CaseSaveFailed` |
```

Use file path and function name; add line numbers only when they are stable. Keep the table to one row per UC element worth verifying, not per line.

## 7. If stories and code both exist

Stories are the intended behavior; code is the actual behavior. Document the intended behavior, verify against the code, and list every mismatch in the reply as "Story says / Code does".

## 8. Reply for reverse-engineered work

Keep the usual reply (UCs produced, open items, key questions) and add one line stating the code paths you read and, under open items, the suspected defects and the inferred rules the user must confirm.
