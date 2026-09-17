## My Lab Notebook for CS1066 PSet #1

Joey Zhang

https://harvard.zoom.us/rec/play/JNPAKptqaV4o9gEiKGUElrPGoLScQrp6zpFKtLfXLwP79ubp8L1B6WVMimE52Lds70GrmX2KBAtQq5YO.0kXV_NjVHAw4WLpj?accessLevel=meeting&canPlayFromShare=true&from=my_recording&continueMode=true&oldStyle=true&componentName=rec-play&originRequestUrl=https%3A%2F%2Fharvard.zoom.us%2Frec%2Fshare%2Fvok_C5gYC3OKsTbPNIlAj1D4ztBL3lFktvpymcxr8as7_HgLMh1RN3frJhP-5tv5.ipNpso2cp3l13b_I)

----
----

### SUBTASK #1: Prompt for the Search Term

----
Text of my first prompt:

please modify trends_save.py so that it can prompt 'Enter a term or a phrase:' in the terminal, and query this word, you can directly modify on top of trends_save.py

Reflections on success/failure of this prompt:

*   I specified which file and change and the goal, and also I specified where to store the modified file.

----
Text of my next prompt:

tell me how to run it in my terminal, starting from creating a virtual environment

Reflections on success/failure of this prompt:

*   I told AI to teach me how to run the code but not directly run it for me, and it followed my instruction.

----
**NOTE:** Delete this text and repeat the above block for as many prompts as it takes to complete this subtask.

----
**FINAL REFLECTION:** Review your work. Write a brief statement of what you might have done differently in hindsight, or defend why your work was a good approach.

I prompted clearly so AI understood me well, but there were some friction when i was trying to set up the virtual environment, something wrong with my local setting, but I solved it with AI's help smoothly.  But I have difficulty reading commands and I'm lack of computer system knowledge so when AI shows me a bunch of commands I always allow it to run, because i don't know what to do anyway.
----
----

### SUBTASK #2: Just One Tool

----
Text of my first prompt:

please create a new file under m02 named my_tool.py, this file needs to combine this functionality of trends_save.py and trends_plot.py, but it does not need to save the csv and read the csv, if possible please make it 'internally' process the data

Reflections on success/failure of this prompt:

I realized what did the notebook mean by 'file clean-up' halfway prompting, so i added the 'but...' sentence, and AI gave me the wanted version in one shot. And this time AI directly told me how to run this file in terminal so i didn't have to ask about it by one more prompt.

----

**FINAL REFLECTION:** Review your work. Write a brief statement of what you might have done differently in hindsight, or defend why your work was a good approach.

I combined the save-and-plot steps into a single, in-memory tool (`m02/my_tool.py`) that prompts for a search term, scrapes the data, and produces a plot. This removed the CSV roundtrip, sped up the workflow, and made it easier to iterate on the data pipeline. Next steps I would take: add CLI flags, stricter input validation, and simple unit tests to make the tool more robust.

----
----

### NEW TASK: Improve the Tool

----
Another idea that aligns with this challenge:

My version of my_tool.py names the image 'interest_the word user entered.png' so I don't have the rename problem. An idea of mine is after getting the data, if the leading one is significantly more than others( mathematically above 1.5* amount of the second one), then we're going to add a small paragraph of explanation of it. The explanation will come from AI. The paragraph should be put in a separate md file, no longer than 500 words. And if there's no significanct detected, we also write a small md file, say that there's no outstanding result founded. The name of the paragraph should be 'the word searched_explanation.md'

----
Which improvement I chose to implement (put an X on the line):

___  The professor's example idea

_X__  My idea above

----
Text of my first prompt:

Let's add one more feature on the top of my_tool.py. After getting the data, if the leading one is significantly more than others( mathematically above 1.5* amount of the second one), then we're going to add a small paragraph of explanation of it. The explanation will come from AI. The paragraph should be put in a separate md file, no longer than 500 words. And if there's no significance detected, we also write a small md file, say that there's no outstanding result founded. The name of the paragraph should be 'the word searched_explanation.md' Name the scraper 'my_new_tool.py'

Reflections on success/failure of this prompt:

The prompt has some weakness: it does not specify where to put the explanation file and my_new_tool.py, and also it does not clarify what does 'amount' stand for. But AI smartly read my mind and finished all the task in one shot. Next time I need to make sure that there's as less undefined space as possible( except for obvious assumptions)
----

**FINAL REFLECTION:** Review your work. Write a brief statement of what you might have done differently in hindsight, or defend why your work was a good approach.

I implemented an improvement that auto-names outputs and detects a significant regional leader, writing a short explanation to a markdown file (`m02/my_new_tool.py`). The feature improves usability and helps interpret results quickly; it attempts to use OpenAI when available and falls back to a clear, evidence-focused paragraph otherwise. An improvement could be add links to any important citation in the explanation file to reduce hallucination.

----
----

### Final Questions

1.  In your own words, give names to the steps in the problem-solving process you followed.

    Understand the problem -- think about solutions -- think about file name and file structure -- prompt and cycle until finished

2.  Which step do you find most challenging, and why?

    File structure, I'm not used to manage files and folders by myself and it needs some 'looking down from top' view to manage the files reasonably.

3.  What two questions do you have about how Python expresses the tasks you might ask it to do?

    I don't know how to load files, read files and operate on csv.  
    I don't know how to write code to automatically ask AI a 'not hard coded' question( which means the question is generated along the code) and paste AI's answer into a file

----
----

### Other's Review

... YOU DO NOTHING HERE; ANOTHER STUDENT WILL COMPLETE THIS PART IN SECTION ...

----
----

### AI's Review

... PASTE AI'S FEEDBACK ON THIS LAB NOTEBOOK HERE ...
