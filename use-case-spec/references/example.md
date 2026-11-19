# Worked example: Submit Case

This is the team's sample UC rewritten in the Markdown template. The alternative and exception flows (AF 1, EF 1) are illustrative additions, to show the expected format; the sample itself had none. The diagram spec that produced the picture is in `example-swimlane.json` (run `python scripts/swimlane.py references/example-swimlane.json out.png`).

---

# 1. Customer Portal

## 1.1. UC 1: Submit Case

| | |
|---|---|
| **Objective:** | This use case allows user to submit Case. |
| **Actor:** | Customer. |
| **Trigger:** | User clicks on "Create New Case" on <<cross reference to Case Listing screen>>. |
| **Pre-condition:** | User logged in successfully as actor above. |
| **Post-condition:** | Case is submitted successfully. |

**Activities Flow**

![UC 1 activities flow](images/uc-01-submit-case.png)

**Alternative Flows**

| Code | Branch Point | Condition | Flow | Rejoin |
|---|---|---|---|---|
| AF 1 | Step (4) | User does not confirm | AF 1.1 User selects "No".<br>AF 1.2 System keeps the entered data and returns to the form. Refer to **BR 2**. | Step (3) |

**Exception Flows**

| Code | Step | Condition | System Response | End State |
|---|---|---|---|---|
| EF 1 | Step (6) | Case cannot be saved (system error) | Display **IEM <TBD>** Case could not be submitted, please try again. Refer to **BR 4**. | User stays on **Screen 2: Case Form screen** with data kept. |

**Business Rules**

| Step | BR Code | Description |
|---|---|---|
| (2) | BR 1 | **Screen Displaying Rules:**<br>The system will load screen: **Screen 2: Case Form screen**. |
| (4) | BR 2 | **Confirmation Message Displaying Rules:**<br>After the User clicks on "Submit" button, the system will display **CFD 1** Are you sure you want to submit Case?.<br>• If User clicks on "No", go to **BR 1**.<br>• If User clicks on "Yes", go to **BR 3**. |
| (6) | BR 3 | **Submitting Rules:**<br>After the User clicks on "Yes" button:<br>• Create a new Case or update existing Case record as follows:<br>&emsp;◦ In case a new Case is created, generate [Case ID] = "CA" + xxxxx<br>&emsp;&emsp;▪ CA: Prefix for Case.<br>&emsp;&emsp;▪ xxxxx: Auto-increment number from 00001 to 99999.<br>&emsp;◦ Update [Assignee] to [Technical Employee ID] of {Technical Employee Profile} that satisfies:<br>&emsp;&emsp;▪ [Team ID] = [Team ID] of {Team} that satisfies [Product] = [Product] of current Case.<br>&emsp;&emsp;▪ [Role] is "Support Engineer".<br>&emsp;&emsp;▪ [Level] is same as [Product Tier] of current Case.<br>&emsp;&emsp;▪ `<Other rules for auto-assigning support engineer>`<br>&emsp;◦ Update [Status] to "Assigned".<br>&emsp;◦ Update [SLA]:<br>&emsp;&emsp;▪ If [Case Severity] is "Major issue", update [SLA] to "1 day".<br>&emsp;&emsp;▪ If [Case Severity] is "Medium issue", update [SLA] to "3 days".<br>&emsp;&emsp;▪ If [Case Severity] is "Minor issue", update [SLA] to "5 days".<br>• Save all changes.<br>• Refer to **CBR 1** to log basic audit trail.<br>&emsp;◦ Append to [Audit Trail] as: Submitted by {Current User Name} at {Current Date Time}.<br>• The system will load screen: **Case List Screen**.<br>• The system will send an email **ET 1**: Sending email to Customer after submitting Case. |
| (6) | BR 4 | **Submit Failure Rules:**<br>If the Case cannot be saved:<br>• Do not create or change any Case record.<br>• Keep the data the User entered on **Screen 2: Case Form screen**.<br>• Display **IEM <TBD>** Case could not be submitted, please try again. |

---

## Notes on what makes this good

- The Trigger names the control and the screen; the screen reference is a `<<...>>` placeholder only because the target screen was not defined yet.
- BR 2 and BR 3 point at each other by code, so the reader can follow the flow without looking at the diagram.
- BR 3 is where precision lives: ID format, assignment criteria, SLA by severity, audit trail text, follow-on screen, email. A developer needs nothing more.
- Unresolved detail is kept visible (`<Other rules for auto-assigning support engineer>`) instead of being silently dropped.
