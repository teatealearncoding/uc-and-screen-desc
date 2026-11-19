# Description wording patterns

Reuse these so every screen reads the same way. Replace the angle-bracket text. In table cells, join lines with `<br>`, start bullets with "•", nest with `<br>&emsp;◦`.

## Dropdown list (value list from data)
```
• Value list: Retrieve all [<Field>] in "<Entity>" that qualifies:
&emsp;◦ [<Field A>] is the same as [<Field A>] of {current user logging in}
&emsp;◦ And [Disable] is "Unchecked".
• Sorting: Alphabetic order.
```
Sorting is always stated. Options: "Alphabetic order", "Ascending order of [<Field>]", "Descending order of [<Field>]". If the list is fixed, write: `Value list: "A", "B", "C".` in display order.

## Dependent (cascading) dropdown
```
• Value list: Retrieve all [<Field>] in "<Entity>" that qualifies:
&emsp;◦ [<Parent ID>] equal [<Parent ID>] of {selected <Parent>}
• If no <Parent> is selected, this field is disabled and empty.
• When <Parent> changes, clear this field.
```
The last two bullets are easy to forget and cause real defects; always state them for cascades.

## Label (derived, read-only)
```
Retrieve [<Field>] in "<Entity>" that qualifies all below conditions:
• [<A>] is [<A>] of {Current user logging in}
• [<B>] is [<B>] of {selected <Thing>}
```
Editable and Mandatory are "N/A".

## Single line / multi lines of text
```
• User inputs <what> of <Record>.
• Max Length: <n> characters.
• When user loses focus of this field and this field is left blank, display **IEM <n>** <Message text>.
```
Add format rules when relevant: allowed characters, pattern, trimming, case.

## Number / date
```
• Allowed range: <min> to <max>.
• Format: <dd/mm/yyyy>.
• If the value is outside the range, display **IEM <n>** <Message text>.
```

## Checkbox / toggle / radio
```
• Value: "Checked" / "Unchecked".
• Default: "<value>".
• When "<value>" is selected, <what changes: show/hide/enable another component>.
```

## Button
```
• This button allows user to <do what>.
• Default is Disabled.
• If all Mandatory fields are filled, the button is enabled.
• Refer to **UC <n>: <Name>**.
```
Drop bullets that do not apply. Trivial buttons get one line:
```
This button allows user to cancel the action.
```
or with data protection:
```
• Close this screen and return to **Screen <n>: <Name> screen**.
• If the user has entered data, display **CFD <n>** <Message text>?.
```

## Toolbar / rich text controls
```
This allows <actor> to format text in field [<Field>].
`<<refer to other part of the document that describes the functions in this Toolbar>>`
```

## Link / tab / menu item
```
• Click to open **Screen <n>: <Name> screen**.
• Visible only to <role>.
```

## Table / grid
```
• Columns: [<A>], [<B>], [<C>].
• Data: Retrieve all {<Record>} that qualify <conditions>.
• Sorting: Descending order of [<Field>].
• Paging: <n> records per page.
• Empty state: display "<message>".
• Row actions: <icon/link> - refer to **UC <n>**.
```

## Visibility and permission (any component)
```
• Show only if <condition>; otherwise hide.
• Editable only when [Status] is "<value>"; otherwise read-only.
```

## When the stories are silent
Draft the row from the mockup only and mark gaps visibly: `Max Length: <TBD>`, `Value list: <TBD>`. List every gap in the reply instead of inventing a rule.
