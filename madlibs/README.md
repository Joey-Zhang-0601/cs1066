Run the second program from the repository root:

```sh
python madlibs/edit.py
```

Write your own title and story. Replace the words you want players to supply
with descriptions inside braces, such as `{adjective}`, `{plural noun}`, or
`{verb ending in -ing}`. Each pair of braces becomes a separate blank.
Finish the story with an empty line, review the preview, and enter `y` to save.

The editor creates `madlibs/stories.json` on the first save and appends later
stories. The file contains a list of objects with `title`, `template`, and
`inputs` fields, using sec03's numbered-placeholder format. An existing
single-story JSON object is also accepted and converted to a list on save.
No stories are supplied automatically; the human designer writes them.

To choose a different JSON file:

```sh
python madlibs/edit.py path/to/stories.json
```

Only Python's standard library is needed.
