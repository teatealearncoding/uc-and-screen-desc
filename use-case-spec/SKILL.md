---
name: use-case-spec
description: Write a Use Case Specification (UC spec) as a Markdown file, with an auto-generated User/System swimlane activity diagram, alternative and exception flows, and a numbered Business Rules table. Use whenever the user asks for a use case spec, use case description, UC document, functional specification, activity flow, or business rules, or hands over user stories, requirements, or mockups and wants them turned into BA documentation, or asks to reverse engineer / document existing code as use cases when no user stories exist - even if they never say "use case". Pairs with the screen-description skill for cross-linked UC and screen documents.
---

# Use Case Specification

Turn user stories (and mockups) into a use case specification a developer and a tester can both build from without asking the analyst anything. The output is Markdown plus one PNG swimlane diagram per use case.

The template below mirrors the team's established UC format. Keep its structure and notation exactly, because readers scan these documents by section and rely on codes (UC, BR, CFD, IEM, ET) to cross-reference. Deviating makes documents inconsistent across a project.

## Workflow

1. **Read the inputs.** User stories give goals, actors and rules. Mockups (view the images) give triggers, buttons, fields and messages. If an uploaded file is not in context, read it first. **If no user stories are provided, switch to reverse engineering** and read the relevant code instead (see "Reverse engineering from code").
2. **Derive the use case list.** One UC per distinct user goal that has its own trigger and its own outcome. Merge story fragments that serve one goal (for example, field-level stories of one form). Split when one story hides two outcomes (for example, Submit and Save as draft are two UCs). Trivial actions such as Cancel or Close become a BR inside the UC that owns them, not a UC.
3. **Plan numbering before writing.** UC numbers are global across the whole document (UC 1, UC 2, ...). Continue from the user's last number if they are appending; otherwise start at 1. If the screen-description skill is also in play, agree the Screen numbers now too, so references match (see "Cross-linking").
4. **Ask only about critical gaps**, in one short batch: unclear actor, unknown trigger, or a missing value that changes the logic (for example SLA thresholds, status transitions, who gets notified). Everything else is drafted with `<TBD>` so the user can review rather than answer a long questionnaire.
5. **Draft each UC** using the template, then **render the diagram** (see "Swimlane diagram").
6. **Run the checklist** at the end, then deliver the files.

## Reverse engineering from code

When there are no user stories, the code is the source. Convert it to the same template; the output must look identical to a story-based spec so readers use one format.

- Find the code (uploads, working directory, or a repository the user names). Scope to the feature or module the user named; if none was named, list the candidates found and ask which to cover.
- Treat each entry point that serves a user goal (route, handler, button action, job, consumer) as a UC candidate, and trace it from entry through authorization, validation, logic, persistence and side effects. Read only the files on that path.
- Document what the code does, not what it should do, in business language with the values kept (formats, limits, statuses, thresholds) and implementation detail left out.
- Separate observed behavior from inferred intent: inferred purpose is written as `<TBD: inferred - ...>`. Report suspected defects, dead code, TODOs and hard-coded values as open items; never silently fix or hide them.
- Append a "Source Traceability" appendix (UC element to file and function) so a reviewer can verify each rule.
- If stories and code both exist, document the intended behavior, verify against the code, and list mismatches as "Story says / Code does".

Read `references/reverse-engineering.md` first: it has the code-to-template mapping table, the tracing procedure and the appendix format.

## Template

Use this structure for every document. Module headings are numbered; UC headings carry the global UC number.

```markdown
# 1. <Module Name>

## 1.1. UC <n>: <Verb + Object>

| | |
|---|---|
| **Objective:** | This use case allows user to <do what>. |
| **Actor:** | <Role(s)>. |
| **Trigger:** | <Exact user action, and the screen it happens on>. |
| **Pre-condition:** | <State that must be true before the UC starts>. |
| **Post-condition:** | <State that is true after success>. |

**Activities Flow**

![UC <n> activities flow](images/uc-<nn>-<slug>.png)

**Alternative Flows**   (omit the section if there are none)

| Code | Branch Point | Condition | Flow | Rejoin |
|---|---|---|---|---|
| AF 1 | Step (3) | <When it applies> | AF 1.1 <User action><br>AF 1.2 <System response, "Refer to BR n"> | Step (4) / End |

**Exception Flows**   (omit the section if there are none)

| Code | Step | Condition | System Response | End State |
|---|---|---|---|---|
| EF 1 | Step (6) | <What goes wrong> | Display **IEM <n>** <message text>. Refer to BR <n>. | <Where the user ends up> |

**Business Rules**

| Step | BR Code | Description |
|---|---|---|
| (2) | BR 1 | **Screen Displaying Rules:**<br>The system will load screen: **Screen 2: Case Form screen**. |
```

A complete worked example (the Submit Case UC) is in `references/example.md`. Read it before writing the first UC in a session; it shows the density and tone expected.

## Section rules

**Header table.** Objective is one sentence starting "This use case allows user to...". Trigger names the concrete control and screen ("User clicks on "Create New Case" on **Screen 1: Case Listing**"), not "User wants to create a case". Pre-condition is a state, not a step ("User logged in successfully as actor above"). Post-condition is the observable end state of the happy path.

**Steps and numbering.** The diagram and the Business Rules table share one numbering scheme, which is what lets a reader jump from a box in the picture to its rule.
- Main flow steps are numbered 1, 2, 3... alternating User and System where natural.
- A choice at one step becomes sub-steps: 5.1 (No), 5.2 (Yes).
- Alternative and exception flow steps use their code: AF 1.1, AF 1.2, EF 1.1.
- The BR table's Step column holds the number of the **system** step the rule implements, in parentheses: (2), (4), (6). User steps carry no rule because users do not execute logic.

**Business Rules** are the single source of truth for system behavior. Anything the system does in the main, alternative or exception flow (display a screen, ask for confirmation, validate, save, assign, notify, log) gets a BR row. Reasons: developers implement from this table and testers derive cases from it, so logic hidden in a flow cell gets missed.
- One BR per system step; give it a bold title ending in a colon: Screen Displaying Rules, Confirmation Message Displaying Rules, Submitting Rules, Validation Rules, Saving Rules, Notification Rules. See `references/br-patterns.md` for wording patterns for each.
- Write bullets inside a table cell with `<br>` and a leading "•"; nest with `<br>&emsp;◦`. Markdown tables cannot hold real lists.
- Branching is explicit and points forward or back by code: "If User clicks on "No", go to **BR 1**."
- State every value that matters: IDs and formats ("CA" + xxxxx, auto-increment 00001 to 99999), statuses, SLA values, who is assigned, what is appended to the audit trail.
- Business rules shared across UCs (audit trail, permission checks) are referenced, never rewritten: "Refer to **CBR 1** to log basic audit trail."

**Alternative vs exception flows.**
- Alternative flow: a valid, different path to the same goal (user cancels, picks another option, saves a draft instead).
- Exception flow: something fails or is rejected (validation error, record locked, service unavailable, no permission). It must say what the user sees (message code and text) and where they end up.
- Every flow names its branch point and where it rejoins or ends. A flow with no rejoin or end state is an unfinished flow.
- If the stories give no alternatives or exceptions, omit those sections. Do not invent them, but if an obvious one is missing (for example an empty required field on a form submit), add it as `<TBD>` and flag it to the user.

## Notation

| Convention | Meaning | Example |
|---|---|---|
| `[Field]` | A data field / attribute | [Case ID], [Status] |
| `{Record or variable}` | An entity, record set, or runtime value | {Team}, {Current User Name} |
| `"Value"` | A literal value or button label | "Assigned", "Submit" |
| `<Placeholder>` | Detail not yet defined | `<Other rules for auto-assigning>` |
| `<TBD>` | Open question to resolve | `CFD <TBD>` |
| **Bold code** | Cross-reference | **Screen 2: Case Form screen**, **BR 3**, **CFD 1** |
| `<<...>>` | Cross-reference target not yet known | `<<cross reference to Case Listing screen>>` |

Codes: **UC** use case, **BR** business rule (numbered per UC, restarting at BR 1), **CBR** common business rule, **CFD** confirmation dialog, **IEM** inline error message, **ET** email template, **AF / EF** alternative / exception flow (per UC).

**Catalog codes (CBR, CFD, IEM, ET).** These come from separate catalogs the team maintains. Reference them; do not redefine them.
- If the user provides the catalog or codes, use them exactly.
- If a code is not given, keep the intended wording and mark the code open: `CFD <TBD>: Are you sure you want to submit Case?`. Never invent a code number, because a made-up code can collide with a real one in the catalog.
- Collect every `<TBD>` code and report them at the end of your reply so the user can assign them.

## Swimlane diagram

Render every UC's activity flow with the bundled script (`scripts/swimlane.py`, relative to this skill). It draws lanes, rounded step boxes, decision diamonds with labelled branches, loop-backs, and start/end markers in the same style as the team's diagrams.

1. Write a JSON spec in the working directory (see the docstring at the top of the script):
   - `lanes`: one per actor role, plus "System" (add an extra lane for an external system if the UC calls one). Use "User" for a single human actor unless the stories use a specific role name; the Actor row still names the role.
   - `nodes`: a `start`, then `step` nodes (`no` = the step number such as "3" or "AF 1.1", `text` = a short verb phrase), `decision` nodes for each branch, and one or more `end` nodes.
   - `edges`: `[from, to]` or `[from, to, "label"]`. Label every edge leaving a decision (Yes, No, or the condition).
2. Run: `python scripts/swimlane.py spec.json images/uc-<nn>-<slug>.png`
3. View the PNG. Check that every numbered box matches a step in the BR table and that no line crosses a box. If layout is crowded, force a node's row with `"row"`, or shorten the text.
4. Show alternative and exception flows in the diagram as branches off the decision where they split, with their code in the step number. An exception that terminates the UC ends at its own `end` node.
5. Keep a diagram to roughly 14 nodes. A bigger flow usually means the UC should be split.

Always write the image path in the Markdown relative to the .md file (`images/...`), and deliver the images alongside the .md.

## Cross-linking

UCs and screens reference each other, so numbering has to agree across both documents.
- Trigger and "load screen" BRs cite the screen: **Screen 2: Case Form screen**.
- If the screen-description skill is used in the same session, use the screen numbers and names it assigns, and the UC numbers it cites on buttons ("Refer to **UC 1: Submit Case**").
- If a screen document already exists (uploaded or earlier in the conversation), read its numbering and reuse it.
- If the target does not exist yet, write `<<cross reference to <name> screen>>` rather than guessing a number.

## Quality checklist (run before delivering)

- Every system step in the diagram has a BR row with a matching Step number, and every BR row maps to a diagram step.
- Every branch has a label, and every flow ends or rejoins somewhere.
- All BR branch references ("go to BR n") point to rows that exist.
- Every UC has Actor, Trigger, Pre-condition, Post-condition filled (or `<TBD>`), and the Post-condition matches what the BRs actually do.
- No invented catalog codes; every missing one is `<TBD>` and listed in the reply.
- Screens and UCs cited in triggers and BRs use the agreed numbers.
- Language is neutral and domain-agnostic in the skill's own text; the specification uses the project's own terms from the stories (or, when reverse engineering, from the UI labels and messages in the code).
- Reverse-engineered documents: every inferred item is marked `<TBD: inferred ...>`, suspected defects are listed in the reply, and the Source Traceability appendix is present.

## Delivery

Save to `/mnt/user-data/outputs/`: `UC_Spec_<Module>.md` plus an `images/` folder with the PNGs, then present the files. In the reply, keep it short: list the UCs produced (number and name), then the open items (`<TBD>` codes and assumptions), then the one or two questions that matter most. For reverse-engineered work, also state the code paths you read, and list suspected defects and inferred rules the user must confirm.
