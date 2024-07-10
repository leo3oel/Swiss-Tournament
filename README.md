# Swiss Tournament

## Setup

### Windows
On windows a python installation is needed download [here](https://www.python.org/downloads/)
 1. Download or clone this repo
 2. Run installRequirements.bat

## Usage
Note: Export to PDF requires a LaTeX installation.

 1. Enter Teams into a `.json`-File (Take `testfile.json` as a template)
 2. Run startGui.bat
 3. Follow the steps in the GUI.
    - Games will be saved automatically after each round.
    - To reopen an existing round use the file with the ending `_Round-xx.json`

## Settings

### Automatically commit to Github Pages
 - Modify the branch name in `HtmlGenerator.py generateHtmlFileMobile()` to the branch where auto commit should be enabled
 - If working on the configured branch a commit will be created after every changed game.
 - The committed files can be displayed via github pages.

 