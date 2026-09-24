## My Lab Notebook for CS1066 PSet #2

Joey Zhang

INSERT-YOUR-VIDEO-LINK (after completing this assignment)

----
----

### Describe Your Decomposition Approach

step1: build a webpage that can accept a company's CIK and retrieve the company's annual revenue, net income and total assets in the past ten years from EDGAR  

step2: then generate 3 vertically stacked plots on the webpage, with year on the x-axis and financial values mentioned above on the y-axis.

----
----

### Document Your Iterations with AI

----

Text of my first prompt:

Work in m04: Build a webpage that accepts a company’s CIK number and retrieves its annual revenue, net income, and total assets for the past ten years from EDGAR. Then generate three vertically stacked plots on the webpage, with year on the x-axis and the corresponding financial values on the y-axis. give the webpage program a reasonable name.
For EDGAR authentication, include the header User-Agent: UniversityStudent your.email@university.edu in every API request.

Reflections on success/failure of this prompt:

*   The AI understood the requested features and authentication requirement without needing clarification.
*   It inspected the existing m04 folder before editing, then chose an approach that fit the small assignment and the patterns already present in the repository.
*   The AI validated its work instead of assuming the first version was correct. A live test exposed an issue with how EDGAR labels revenue, and the AI revised its approach after that test.
*   The prompt could have explicitly requested error handling, responsive design, and testing, but the AI inferred those useful additions from the task.

----

Text of my next prompt:

> Add a feature to the m04 webpage so that users can enter a company's name instead of knowing its CIK number. Use SEC company records to find the corresponding CIK number and official company name, display them together as a pair, and let the user use the CIK to retrieve the company's financial charts. Keep the required User-Agent header in every EDGAR API request.

Reflections on success/failure of this prompt:

*   This prompt adds a more realistic way for users to identify a company because most users will not know its CIK number.
*   It clearly explains the desired result of the lookup: the official company name and CIK should be displayed together.
*   It also connects the new lookup to the original chart workflow instead of replacing it.
*   The prompt could have specified how to handle several possible name matches, but the AI was able to choose a reasonable matching approach.

----

**NOTE:** Delete this text and repeat the above block for as many prompts as it takes to complete the pset.

----

**FINAL REFLECTION:** Review your prompting work. How does your work on this pset compare with that of the first pset?

I could have mentioned a few additional requirements:

*   How invalid CIK numbers and missing EDGAR data should be handled.
*   That the program should test the API with a sample CIK after implementation.
*   Whether the charts should use lines or bars and how large financial values should be formatted.
*   How to handle multiple companies with similar names.

----
----

### Handling the Problem's Whitespace

When you have a working solution, write a brief statement describing how you ultimately approached the problem's whitespace. What you might have done differently in hindsight, and why? Or defend why your work was a good approach.

Filled:

*   Company-name lookup returning the official name and CIK together
*   CIK input and EDGAR retrieval
*   Revenue, net income, and total assets
*   Ten years of annual data
*   Three vertically stacked plots and the required User-Agent header

Not filled:

*   Exact chart style, formatting, error handling, and multiple-name-match behavior were not specified.


----
----

### Other's Review

... YOU DO NOTHING HERE; ANOTHER STUDENT WILL COMPLETE THIS PART IN SECTION ...

----
----

### AI's Review

... PASTE AI'S FEEDBACK ON THIS LAB NOTEBOOK HERE ...
