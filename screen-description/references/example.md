# Worked example: Case Form screen

This is the team's sample screen description rewritten in the Markdown template. The image shown is the mockup with numbered callouts already on it, so the # column matches the picture.

---

## 2. Create Case Screen

- This screen allows user to Save case as Draft or Submit Case.
- User can access this screen by: Click on "New case" on **Screen <TBD>**.

![Case Form screen mockup](images/screen-02-case-form.png)

**Screen 2: Case Form screen**

| # | Component | Comp. Type | Editable | Mandatory | Default Value | Description |
|---|---|---|---|---|---|---|
| 1 | Product | Dropdown list | Yes | Yes | N/A | • Value list: Retrieve all [Product] in "Subscription" that qualifies:<br>&emsp;◦ [Customer ID] is the same as [Customer ID] of {current user logging in}<br>&emsp;◦ And [Disable] is "Unchecked".<br>• Sorting: Alphabetic order. |
| 2 | Product Version | Dropdown list | Yes | Yes | N/A | • Value list: Retrieve all [Product Version Name] in "Product Version" that qualifies:<br>&emsp;◦ [Product ID] equal [Product ID] of {selected Product}<br>&emsp;◦ and [Disable] is "Unchecked".<br>• Sorting: Ascending order of [Release Datetime]. |
| 3 | Product Tier | Label | N/A | N/A | N/A | Retrieve [Product Tier] in "Subscription" that qualifies all below conditions:<br>• [Customer ID] is [Customer ID] of {Current user logging in}<br>• [Product ID] is [Product ID] of {selected Product}<br>• [Product Version ID] is [Product Version ID] of {selected Product Version}. |
| 4 | Case Severity | Dropdown list | Yes | Yes | N/A | • Value list: Retrieve all [Case Severity Name] in "Case Severity" that qualifies [Disable] is "Unchecked".<br>• Sorting: Alphabetic order. |
| 5 | Title | Single Line of Text | Yes | Yes | N/A | • User inputs Title of Case.<br>• Max Length: 50 characters.<br>• When user loses focus of this field and this field is left blank, display **IEM 1** Please input in this field. |
| 6 | Toolbar | Toolbar | N/A | N/A | N/A | This allows Customer to format text in field [Description].<br>`<<refer to other part of the document that describes detail about all the functions in this Toolbar>>` |
| 7 | Description | Multi lines of text | Yes | Yes | N/A | • User inputs Description of Case.<br>• Max Length: 2000 characters<br>• When user loses focus of this field and this field is left blank, display **IEM 1** Please input in this field. |
| 8 | Submit | Button | N/A | N/A | N/A | • This button allows user to submit Case.<br>• Default is Disabled.<br>• If all Mandatory fields are filled, the button is enabled.<br>• Refer to **UC 1: Submit Case**. |
| 9 | Save as draft | Button | N/A | N/A | N/A | This button allows user to save Case as draft, refer to `<<cross reference to the corresponding use case>>` |
| 10 | Cancel | Button | N/A | N/A | N/A | This button allows user to cancel the action. |

---

## Notes on what makes this good

- Every control on the mockup has one row, numbered to match the callouts.
- Dropdowns always give source entity, filter conditions and sort order. Developers should never have to guess the query.
- Dependent controls state their dependency ({selected Product} drives Product Version and Product Tier).
- Product Tier is a Label: derived and read-only, so Editable and Mandatory are N/A.
- Inline validation names the trigger (loses focus), the condition (left blank) and the message (**IEM 1** plus text).
- The Submit button states its enable rule and cites its UC instead of repeating the submit logic.
- Open links stay visible as `<TBD>` or `<<...>>` placeholders, never silently dropped.
- Cancel is trivial, so it is described in one line. A stricter spec would add the unsaved-data confirmation (**CFD <TBD>**).
