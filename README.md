# Desktop utility by [Facel](https://facel.tech)

[Fork this repo](https://github.com/facel-tech/desktop-utility/fork)
|
[Visit website](https://facel.tech)

![illustration](./illustration.png)

This project contains source code of the desktop utility, a substantial part of Facel. 

[Facel](https://facel.tech) is an AI-based stress reduction app that uses behavioral and physiological data to understand how you feel.


## Installation

Go to [this Notion page](https://facel.notion.site/Changelog-8c1d2d1edce249579de283425e42a4b6) to check the last available build of the package.

## How does it work?

[Facel](https://facel.tech) uses ML to process data (facial expressions, typing patterns, musical preferences, and weather conditions) to prevent stress and fatigue at its very core.


**Functions:**

1. Facel disables notifications and sends replies to colleagues when the user is busy or stressed.
2. Team members can see each other emotional states in real-time.
3. Facel selects music that fits the user's emotional state.
4. Facel gives recommendations on how to feel better.


## What is desktop utility?

It is an app that catches your typing patterns so that [Facel](https://facel.tech) can analyze them and understand your emotional state.

**The most interesting parts for you:**
- [Keystroke listener](https://github.com/facel-tech/desktop-utility/blob/main/python/listeners/keyboard.py) monitors the keyboard events.
- [Mouse listener](https://github.com/facel-tech/desktop-utility/blob/main/python/listeners/mouse.py) monitors the mouse events.
- [Mouse processor](https://github.com/facel-tech/desktop-utility/blob/main/python/processors/mouse.py) computes various statistics of mouse events.
- [Keystroke rates processor](https://github.com/facel-tech/desktop-utility/blob/main/python/processors/keystroke.py) processes keystroke timestamps to figure out the occurrences of backspace, punctuation, and other stuff.
- [Keystroke combinations processor](https://github.com/facel-tech/desktop-utility/blob/main/python/processors/timing.py) processes keystroke timestamps to get mean and standard deviation of latencies between the presses of different combinations of keystrokes.

## Can I become a contributor?

Glad you asked (because we actually need contributors).

The app is written on [pyqt](https://pypi.org/project/PyQt6/), so it is cross-platform.

**Some tasks for you to consider:**

- Test this app on Windows machine (because we all are Mac users) and fix it.
- Fix project structure.
- (...) Whatever you consider important.


## I have some question, who should I contact?

Write to [Denis](mailto:mixeden@facel.tech) in case you want some specific questions or you just want an invite code to Facel.
