---
name: screen-description
description: Write a Screen Description (UI specification) as a Markdown file - purpose, access path, the mockup with numbered callouts, and a component table (Component, Type, Editable, Mandatory, Default Value, Description). Use whenever the user shares mockups, wireframes or UI screenshots and wants them documented, or asks for a screen spec, screen description, UI spec, field list or component table, or hands over user stories plus mockups for BA documentation, or asks to reverse engineer / document existing UI code as screen descriptions when no stories or mockups exist - even if they never say "screen description". Pairs with the use-case-spec skill for cross-linked UC and screen documents.
---

# Screen Description

Turn a mockup (plus user stories) into a screen specification that tells a developer exactly what every control is, how it behaves, and what data it shows, and tells a tester what to check. The output is Markdown; the mockup image is embedded when provided.

The template mirrors the team's established format. Keep its structure and notation, because readers jump between this document and the use case spec using the same numbers and codes.

## Workflow

1. **Read the inputs.** View every mockup image. The mockup is the source of truth for *what components exist*; the user stories are the source of truth for *how they behave* (rules, values, validation). **If no user stories are provided, switch to reverse engineering** and read the relevant UI code instead (see "Reverse engineering from code").
2. **Plan numbering.** Screen numbers are global across the whole document (Screen 1, Screen 2, ...). Continue from the user's last number if appending; otherwise start at 1. If the use-case-spec skill is also in play, agree UC numbers now too (see "Cross-linking").
3. **Inventory the components.** List every visible control on the mockup: fields, dropdowns, labels, toolbars, buttons, links, tabs, tables/grids, icons that act. Do not skip chrome that behaves (a rich-text toolbar, a collapse arrow). Skip pure decoration and the browser frame.
4. **Number the components.** If the mockup already has numbered callouts, use those numbers exactly. If not, number in reading order: input fields first (top to bottom, left to right within each group), then toolbars, then action buttons last. Then add callouts to the image (see "Mockup image").
5. **Write each component's row**, using the patterns in `references/description-patterns.md`.
6. **Ask only about critical gaps**, in one short batch: where a value list comes from, what a button does when the story is silent, mandatory-ness that is not visible on the mockup. Everything else is drafted with `<TBD>` so the user reviews rather than answers a questionnaire.
7. **Run the checklist**, then deliver.

## Reverse engineering from code

When there are no user stories, the code is the source. Convert it to the same template; the output must look identical to a story-based spec so readers use one format.

- Find the code (uploads, working directory, or a repository the user names). Work one screen at a time. If the user named a screen or feature, start there; otherwise list the screens found (from routes and navigation) and ask which to cover.
- Build the component table from the screen's markup or form definition: label, control type, disabled/readonly state, required flag, default, value-list source with filter and sort, limits and formats, validation messages, button handlers, and the route and menu entry that reach the screen. Read only that screen's files and what it directly uses.
- Document what the code does, not what it should do, in business language with the values kept (limits, formats, defaults) and implementation detail left out.
- Code gives no picture: use the mockup placeholder, number components in reading order, and tell the user callouts are needed once a mockup exists.
- Separate observed behavior from inferred intent: inferred purpose is written as `<TBD: inferred - ...>`. Report suspected defects (for example UI and API limits that disagree), dead controls and hard-coded options as open items; never silently fix or hide them.
- Append a "Source Traceability" appendix (item to file and component) so a reviewer can verify each row.
- If stories or mockups also exist, document the intended design, verify against the code, and list mismatches as "Design says / Code does".

Read `references/reverse-engineering.md` first: it has the code-to-column mapping table and the appendix format.

## Template

```markdown
## <Section no>. <Screen Name> Screen

- This screen allows user to <purpose>.
- User can access this screen by: <path - the control and the screen it is on>.

![<Screen name> mockup](images/screen-<nn>-<slug>.png)

**Screen <n>: <Screen name> screen**

| # | Component | Comp. Type | Editable | Mandatory | Default Value | Description |
|---|---|---|---|---|---|---|
| 1 | Product | Dropdown list | Yes | Yes | N/A | <rules> |
```

A full worked example (the Case Form screen) is in `references/example.md`. Read it before writing the first screen in a session.

## Section rules

**Heading and intro.** Section number is the running section in the document; screen number is the global Screen n. They differ and both appear (section "2. Create Case Screen", then "Screen 2: Case Form screen") because sections group by feature while Screen numbers are what the UC spec cites. Intro bullet 1 says what the screen is for in one sentence. Intro bullet 2 gives the real access path ("Click on "New Case" on **Screen 1: Case List screen**"), because testers need to know how to reach the screen.

**The # column** matches the numbered callouts on the image. Order rows by #.

**Component** is the label as shown on the mockup (use the visible text, including button labels). For unlabelled controls, use a short functional name: "Rich text toolbar", "Description input".

**Comp. Type**, use one of: Dropdown list, Multi-select dropdown, Single Line of Text, Multi lines of text, Rich Text Editor, Number, Date, Date Time, Checkbox, Radio group, Toggle, Label, Link, Button, Toolbar, Table, Tab, Icon, File upload. Keep the exact wording above (it matches the team's existing documents). Pick the closest; add a new type only if none fits. A toolbar may be typed "Toolbar" or "N/A"; use "Toolbar" unless the user's documents say otherwise.

**Editable** and **Mandatory**: "Yes" or "No". Use "N/A" where the idea does not apply (buttons, labels, toolbars, tabs). Mandatory comes from the red asterisk on the mockup or from the stories. An asterisk the mockup shows but the stories contradict is an open question: pick the mockup, flag it.

**Default Value**: the exact value, or "N/A" when none. Derived defaults go in the Description, with "N/A" here only if nothing is preselected.

**Description** is the substance. One rule per bullet; write in the same style as the use case spec's business rules. Required elements, when they apply:
- Where the data comes from (value lists, labels) and how it is filtered and sorted.
- Dependencies on other components (cascading lists, enable/disable conditions).
- Limits and formats (max length, allowed characters, date format).
- Validation with the inline message code and text.
- What a button does and which UC it triggers.
- Visibility and permission conditions.
Use `<br>` between bullets and start each with "•"; nest with `<br>&emsp;◦`. Markdown table cells cannot hold lists.

Every behavior that is more than a single-screen rule belongs to the UC. Describe it here only as "Refer to **UC <n>: <Name>**", so the logic lives in one place.

## Notation

| Convention | Meaning | Example |
|---|---|---|
| `[Field]` | A data field / attribute | [Product], [Status] |
| `{Record or variable}` | An entity or runtime value | {Product}, {Current User} |
| `"Value"` | A literal value or label | "Submit", "Major issue" |
| `<TBD>` / `<Placeholder>` | Open or undefined detail | `<other filter rules>` |
| **Bold code** | Cross-reference | **UC 1: Submit Case**, **IEM 1**, **CFD 1** |
| `<<...>>` | Cross-reference target not yet known | `<<cross reference to Subscription screen>>` |

Codes: **IEM** inline error message, **CFD** confirmation dialog, **CBR** common business rule, **ET** email template, **UC** use case, **Screen n** screen.

**Catalog codes (IEM, CFD, CBR, ET)** come from separate catalogs the team maintains. Reference them; do not redefine them.
- If the user provides the catalog or codes, use them exactly.
- If a code is not given, keep the intended wording and mark the code open: `IEM <TBD>: Please input in this field.` Never invent a code number, because it can collide with a real one in the catalog.
- Report every `<TBD>` code at the end of your reply.

## Mockup image

- **Image provided:** copy it to `images/screen-<nn>-<slug>.png` (convert other formats to PNG) and embed it.
- **Image already has numbered callouts:** use them as is. Make the table's # column match.
- **Image has no callouts:** run `scripts/annotate.py` (relative to this skill) with a JSON list of `{"n", "x", "y"}` pixel coordinates, placing each circle just to the right of its component. View the result and fix any circle that covers a control or sits by the wrong one. Do this once; do not iterate beyond one correction pass.
- **No image provided:** insert a placeholder line in place of the image, and still produce the component table from the stories:
  `> [Mockup placeholder: <Screen name> - insert image here and align callout numbers with the # column]`
  Number components in reading order and tell the user the callouts will need to be added.

Always write image paths relative to the .md file and deliver the images alongside it.

## Cross-linking

Screens and UCs reference each other, so numbering has to agree across both documents.
- Buttons and links that start a process cite the UC: "Refer to **UC 1: Submit Case**".
- The access path cites the screen the user comes from.
- If the use-case-spec skill is used in the same session, use the UC numbers and names it assigns; if a UC document already exists (uploaded or earlier in the conversation), read its numbering and reuse it.
- If the target does not exist yet, write `<<cross reference to <name> use case>>` rather than guessing a number.
- Buttons whose entire behavior is trivial (Cancel, Close) are described here in full ("Close the screen and return to **Screen 1: Case List screen**. Refer to **CFD <TBD>** if data was entered") and need no UC.

## Quality checklist (run before delivering)

- Every visible component on the mockup has exactly one row; every row has a callout (or a placeholder note).
- # numbers are unique, ascending, and match the image.
- Every dropdown has a data source and sort order; every text input has a limit or `<TBD>`; every mandatory field has a validation message (code or `<TBD>`).
- Every button states what it does and cites its UC or its trivial behavior.
- Access path is a real path, not "from the menu".
- No invented catalog codes; every missing one is `<TBD>` and listed in the reply.
- Language is neutral; use the project's own terms from the stories (or, when reverse engineering, from the UI labels and messages in the code).
- Reverse-engineered documents: every inferred item is marked `<TBD: inferred ...>`, suspected defects are listed in the reply, and the Source Traceability appendix is present.

## Delivery

Save to `/mnt/user-data/outputs/`: `Screen_Description_<Module>.md` plus an `images/` folder, then present the files. In the reply, keep it short: list the screens produced (number and name), then the open items (`<TBD>` codes and assumptions, whether callouts were added), then the one or two questions that matter most. For reverse-engineered work, also state the code paths you read, and list suspected defects and inferred behavior the user must confirm.
