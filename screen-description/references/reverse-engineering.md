# Reverse engineering a Screen Description from code

Use this when no user stories or mockups are provided, or the user points at a codebase and asks for screen documentation. The goal is a component table a business reader can verify, written from what the UI code actually renders and does.

## 1. Find the code and fix the scope

- Look in the places the code is likely to be: `/mnt/user-data/uploads`, the working directory, or a repository the user names (cloning from github.com is allowed in this environment). If you cannot find it, ask for the location in one short question.
- One screen at a time. If the user named a screen, route or feature, start there. If not, list the screens you found (from the route table, navigation menu, page/view folders) grouped by module, and ask which to cover or propose a first batch.
- Search first (routes, page components, view templates), then read only the files for that screen and what it directly uses (child components, form schemas, validators, API calls).

## 2. Locate the screen's pieces

| Piece | Where to look |
|---|---|
| Screen definition | Route table, page/view component, template (`.cshtml`, `.html`, `.jsx/.tsx`, `.vue`, `.xaml`, `.razor`, `.erb`, `.blade.php`, Android/iOS layouts) |
| Fields and layout | Markup, form builders, form definitions or schemas, config-driven forms |
| Value lists | API calls, repository/service queries, enum or lookup sources bound to selects |
| Validation | Form validators, schema rules (Yup, Zod, FluentValidation, Bean Validation annotations, model attributes), inline checks in handlers |
| Behavior | Event handlers (change, blur, click, submit), watchers, state logic, enable/disable conditions |
| Text | Labels and messages in i18n/resource files |
| Access | Navigation menu entries, links to this route, route guards and permission checks |

## 3. Map code to the component table

| Column | Source in code |
|---|---|
| Component | The visible label (from markup or i18n). If unlabelled, a short functional name. |
| Comp. Type | Control used: `select` = Dropdown list, `input type=text` = Single Line of Text, `textarea` = Multi lines of text, rich editor = Rich Text Editor, `button` = Button, `checkbox`, date picker, grid, and so on. Use the skill's type vocabulary. |
| Editable | `disabled`/`readonly`/read-only bindings, conditions that lock the field. Label-like display of derived data is "N/A". |
| Mandatory | `required` attributes, validator "required" rules, schema `.required()`, `[Required]`, or an asterisk in markup. |
| Default Value | Initial state, default props, preselected option, model defaults. |
| Description | Value list source, filter and sort, max length and format (`maxlength`, pattern, validator limits), dependencies (watchers, cascading selects), validation messages, enable/disable rules on buttons, the handler's effect and the use case it belongs to, visibility or permission conditions. |
| Access path (intro bullet 2) | The menu item, link or button that navigates to the route, and the screen it sits on. |
| Component order and # | No mockup: reading order of the markup, input fields first, then toolbars, then action buttons last. |

## 4. Write what the code does, in business language

- Describe observed behavior, not what you think it should do. If the code and common sense disagree, the spec follows the code and the discrepancy is reported.
- Use the user-visible label for a field; mention a property or column name only when there is no label.
- Keep implementation out of descriptions (no component names, hook names, SQL). Keep **values** in: limits, formats, filters, sort order, defaults, thresholds.
- Resolve enums and option values to the text the user sees. Dynamic options loaded from a database you cannot see: describe the query ("Retrieve all [X] in "Y" that qualifies ...") and mark contents `<TBD>`.
- Message codes: use the message text from the code. Use the team's catalog code if the user supplies one; otherwise `IEM <TBD>` / `CFD <TBD>` with the text. Never invent a code number.
- Button logic bigger than a screen rule (create, save, notify, assign) is a use case. Write "Refer to **UC <n>: <Name>**" and, if the use-case-spec skill is also in play, document the logic there.

## 5. No mockup: placeholder, not guesswork

Code cannot give you a picture. Do not try to render or imitate a mockup. Insert the placeholder line from the main skill instructions, number components in reading order, and tell the user callouts will need to be added when a screenshot or mockup is available. If the user later provides an image, run the callout helper and align the # column.

## 6. Distinguish fact from inference

- **Observed:** read directly in code. Write it plainly.
- **Inferred:** a purpose you deduced. Write it as `<TBD: inferred - <what you think>>` or ask in the reply.

Report as open items, never silently fix or hide:
- Likely defects: a field required in the UI but not validated on the server (or the reverse), mismatched limits between UI and API, unreachable states.
- Dead or commented-out controls, `TODO`/`FIXME` notes that change behavior.
- Hard-coded options that look like they should come from data.
- Behavior depending on data, config or feature flags you could not see.

## 7. Source traceability appendix

Append a short table at the end of the .md for reverse-engineered documents:

```markdown
## Appendix: Source Traceability

| Item | Source |
|---|---|
| Screen 2 access path | `src/routes.tsx` - `/cases/new`; `CaseList.tsx` - "New case" button |
| # 1 Product (value list) | `CaseForm.tsx` - `useProducts()`; `ProductService.ts` - `listForCustomer()` |
| # 5 Title (max length 50) | `caseSchema.ts` - `title` rule |
```

Use file path plus function or component name; add line numbers only when stable. One row per item worth verifying, not per line.

## 8. If stories or mockups also exist

Stories and mockups are the intended design; code is the actual behavior. Document the intended design, verify against the code, and list every mismatch in the reply as "Design says / Code does".

## 9. Reply for reverse-engineered work

Keep the usual reply (screens produced, open items, key questions) and add one line stating the code paths you read, and under open items the suspected defects and inferred behaviors the user must confirm.
