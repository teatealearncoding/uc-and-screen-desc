# Business Rule wording patterns

Reuse these patterns so every UC reads the same way. Replace the angle-bracket text. Keep one BR per system step, with a bold title ending in a colon. In tables, join lines with `<br>`, start bullets with "•", nest with `<br>&emsp;◦` then `<br>&emsp;&emsp;▪`.

## Screen Displaying Rules
Use when the system shows a screen or a state of it.

```
**Screen Displaying Rules:**
The system will load screen: **Screen <n>: <Name> screen**.
```
Add data-loading conditions only when they change what is shown:
```
• Display only {Cases} that satisfy [Customer ID] = [Customer ID] of {Current User}.
• Sort by [Created Date] descending.
```

## Confirmation Message Displaying Rules
Use when the user must confirm before the system acts.

```
**Confirmation Message Displaying Rules:**
After the User clicks on "<Button>" button, the system will display **CFD <n>** <Message text>?.
• If User clicks on "No", go to **BR <n>**.
• If User clicks on "Yes", go to **BR <n>**.
```
Unknown code: `**CFD <TBD>** <Message text>?`

## Validation Rules
Use for checks that run on submit or on a step transition. Field-level inline checks belong in the screen description; repeat here only if the UC enforces them again.

```
**Validation Rules:**
The system validates the data entered:
• If [<Field>] is blank, display **IEM <n>** <Message text> and stop.
• If [<Field>] is not in format <format>, display **IEM <n>** <Message text> and stop.
• If all checks pass, go to **BR <n>**.
```

## Submitting / Saving Rules
Use when the system creates or updates records. Be exact about values.

```
**Submitting Rules:**
After the User clicks on "<Button>" button:
• Create a new {<Record>} or update the existing one as follows:
&emsp;◦ In case a new record is created, generate [<ID>] = "<prefix>" + xxxxx
&emsp;&emsp;▪ <prefix>: Prefix for <Record>.
&emsp;&emsp;▪ xxxxx: Auto-increment number from 00001 to 99999.
&emsp;◦ Update [Status] to "<Status>".
• Save all changes.
```

## Assignment / Derivation Rules
Use when a value is computed or picked from other data.

```
• Update [<Field>] to [<Field>] of {<Record>} that satisfies:
&emsp;◦ [<A>] = [<A>] of <source>.
&emsp;◦ [<B>] is "<Value>".
&emsp;◦ `<Other rules>`
```
Use "If ... update ... to ..." lines when the result depends on a value:
```
• If [Case Severity] is "Major issue", update [SLA] to "1 day".
```

## Status Transition Rules
```
**Status Update Rules:**
• Update [Status] from "<From>" to "<To>".
• Only users with <role> can perform this transition. Otherwise display **IEM <n>** <Message>.
```

## Notification Rules
```
**Notification Rules:**
• The system will send an email **ET <n>**: <Purpose of email>.
&emsp;◦ To: <recipient and how it is derived>.
&emsp;◦ Trigger: <when>.
```

## Audit and Common Rules
Never rewrite a common rule; cite it.
```
• Refer to **CBR <n>** to log basic audit trail.
&emsp;◦ Append to [Audit Trail] as: <text> by {Current User Name} at {Current Date Time}.
```

## Failure Rules (use in exception flows)
```
**<Action> Failure Rules:**
If <what fails>:
• Do not create or change any <Record>.
• Keep the data the User entered on **Screen <n>: <Name> screen**.
• Display **IEM <n>** <Message text>.
```

## Style notes
- Name the condition before the action: "If X, do Y." Avoid "should"; use present tense ("the system will" or imperative).
- Quote literal values ("Assigned"); bracket fields ([Status]); brace records ({Team}).
- If a value or rule is not decided, write it as `<TBD>` or `<Other rules for ...>` and keep it visible.
- If a rule is longer than about 15 lines, check whether it is really two steps and split it.
