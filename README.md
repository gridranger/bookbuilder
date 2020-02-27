# Book Builder

## Usage

Run it with `python main.py manuscripts/folder file/to/save/without/extension`

## Structure

Manuscripts could be placed into a single folder or placed into a tree structure. Subfolders under the manuscript folder will be used as Heading 1 (H1) chapters in the chapter hierarchy. Subfolders under them will be H2 and so on. Headings inside files will be demoted to one level lower then their parent chapter.

Example:
```/
+-- Part 1
|   +-- Chapter 1.md
|   +-- Chapter 2.md
+-- Part 2
|   +-- Chapter 3.md
+-- Epilogue.md
```

Folders Part 1 and 2 will be H1 titles. H1 titles in chapter 1, 2 and 3 will be converted to H2 titles (demoted by one). Epilogue's title will not be demoted as it is at the manuscripts folder directly.

## Format

It could be designed by editing `templates/stylesheet.css`. Currently paragraph settings are set according to the Hungarian publishing tradition but could be changed freely.

Markdown will be processed with smarty-pants flavor (https://daringfireball.net/projects/smartypants/)

## Installation

Requires Python v3.7. Create a venv, activate it and install requirements with `pip install -r requirements.txt`
