[![Release](https://github.com/mperezi/alfred-git-clone/workflows/Release/badge.svg)](https://github.com/mperezi/alfred-git-clone/actions?query=workflow%3ARelease)

# alfred-git-clone

An [Alfred workflow](https://www.alfredapp.com/workflows/) to clone git repos like a *master* 🐑🐑

![alfred-git-clone](https://user-images.githubusercontent.com/43891734/93094028-acf31200-f6a1-11ea-9a23-8379f45040dd.gif)

## Install

Download the latest version from [Releases](https://github.com/mperezi/alfred-git-clone/releases) and double click the downloaded file to install it.

## Usage

1. Copy the repo URL to the clipboard.
2. Open Alfred and start typing the keyword *clone* to trigger the workflow.
3. Confirm the repo you're about to clone by pressing <kbd>enter</kbd> or press <kbd>⌥</kbd>+<kbd>enter</kbd> to choose a different name.
4. Browse your *workspace* and pick a destination folder. Start typing for filtering and then hit <kbd>tab</kbd> to drill into the selected folder or <kbd>enter</kbd> to clone into it.
5. Wait until a notification pops up letting you know about the outcome of the operation. In case of success a terminal window will open inside the repo you just cloned.

## Features

### Forgiveness

If you carelessly copy over some items on top of your URL your repo will still be found. More specifically the last ten entries of your clipboard are scraped to look for valid git repos.

### History

After some usage you will start seeing your most frequently used directories when browsing your workspace.

## Settings

The following variables are meant to be set in the [workflow configuration sheet](https://www.alfredapp.com/help/workflows/advanced/variables/#environment):

* `workspace_dir`: the path of the root folder where all your projects live (default:`$HOME`)
* `max_recent_items`: max number of history items to show (default: 2)

## Acknowledgements

This workflow uses the awesome 😎 [Alfred-Workflow](http://www.deanishe.net/alfred-workflow/) Python library by [deanishe](https://www.alfredforum.com/profile/5235-deanishe/).

Sheep icon provided by [Stockio.com](https://www.stockio.com/).