"""Let a human write Mad Libs stories and save them in a JSON collection."""

import argparse
import json
from pathlib import Path
import re


DEFAULT_FILE = Path(__file__).with_name("stories.json")


def make_story(title, text):
    """Convert human-written {word descriptions} to numbered placeholders."""
    if not title.strip() or not text.strip():
        raise ValueError("Please provide both a title and a story.")
    if re.search(r"\[\d+\]", text):
        raise ValueError("Use {noun}-style blanks instead of numbered brackets.")
    inputs = {}

    def replace_blank(match):
        description = match.group(1).strip()
        if not description:
            raise ValueError("Each blank needs a description, such as {verb}.")
        key = str(len(inputs))
        inputs[key] = description
        return f"[{key}]"

    template = re.sub(r"\{([^{}]*)\}", replace_blank, text)
    if "{" in template or "}" in template:
        raise ValueError("Check your braces: each blank should look like {noun}.")
    if not inputs:
        raise ValueError("Add at least one blank, such as {adjective}.")
    return {"title": title.strip(), "template": template, "inputs": inputs}


def load_stories(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as source:
        stories = json.load(source)
    # Accept the single-story format shown in sec03 as well as a list.
    if isinstance(stories, dict):
        stories = [stories]
    if not isinstance(stories, list) or not all(
        isinstance(story, dict)
        and isinstance(story.get("title"), str)
        and isinstance(story.get("template"), str)
        and isinstance(story.get("inputs"), dict)
        for story in stories
    ):
        raise ValueError("The JSON file must contain a story or a list of stories.")
    return stories


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, default=DEFAULT_FILE,
                        help="JSON file to add stories to (default: stories.json beside edit.py)")
    path = parser.parse_args().file

    print("Mad Libs Story Studio")
    print("Write your own story and choose the blanks with curly braces.")
    print("Replace each chosen word with a description: {noun}, {verb ending in -ing}, etc.")
    print("Enter multiple lines if you like; finish with an empty line. Ctrl+C cancels.\n")

    while True:
        title = input("Story title: ").strip()
        print("Your story:")
        lines = []
        while True:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        try:
            story = make_story(title, "\n".join(lines))
        except ValueError as error:
            print(f"\n{error} Let's try again.\n")
            continue

        print(f"\nPreview: {story['title']}\n{story['template']}")
        for key, description in story["inputs"].items():
            print(f"  [{key}]: {description}")
        if input("Save this story? [y/N]: ").strip().lower() in ("y", "yes"):
            # Reload before saving so existing stories are retained.
            stories = load_stories(path)
            stories.append(story)
            with path.open("w", encoding="utf-8") as destination:
                json.dump(stories, destination, indent=2, ensure_ascii=False)
                destination.write("\n")
            print(f"Saved! {path.resolve()} now contains {len(stories)} story/stories.")
        else:
            print("Story discarded.")
        if input("Create another story? [y/N]: ").strip().lower() not in ("y", "yes"):
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
    except (OSError, ValueError) as error:
        raise SystemExit(f"Could not save the story: {error}")
