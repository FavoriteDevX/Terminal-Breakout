# Terminal Breakout Game

A fully playable, lightweight, and zero-dependency **Breakout clone** made to run entirely inside your command-line interface. Written in pure Python using standard built-in modules.

This version features **decoupled game physics**, meaning your paddle movement is completely lag-free and instant, while the ball glides smoothly at an arcade pace. It also includes full retro ANSI terminal color support.

No external package managers like `npm`, `node`, or `pip` are required!

## Features
- **Zero-Dependency:** Runs on vanilla Python 3.x using only core libraries (`sys`, `os`, `time`, `random`).
- **Cross-Platform:** Native Windows support (PowerShell/CMD) using standard ANSI virtual terminal sequences, as well as Linux/macOS.
- **Instant Controls:** Frame-decoupled input system ensures the paddle moves without any artificial latency.
- **Retro Graphics:** Multi-colored brick layers (Red, Green, Yellow) built entirely out of text characters.

## Installation & Running

1. **Copy the script:** Save the game code into a file named `breakout.py`.
2. **Run the game:** Open your preferred terminal emulator, navigate to the directory where the file is saved, and execute:
   ```bash
   python breakout.py
   ```
   *(On some systems, you might need to use `python3 breakout.py`)*

## Game Controls

- **A** or **Left Arrow Key**: Move paddle left (instant feedback)
- **D** or **Right Arrow Key**: Move paddle right (instant feedback)
- **R**: Restart the game (available on *Game Over* or *Victory* screens)
- **Q**: Instantly close and quit the game back to the terminal prompt

<img width="619" height="466" alt="Screenshot 2026-10-25 165047" src="https://github.com/user-attachments/assets/1d2abefe-8a94-4a89-9614-8cf43f5454f7" />

<img width="604" height="458" alt="Screenshot 2026-10-25 165103" src="https://github.com/user-attachments/assets/35433574-de42-42b4-b411-530b34d4c526" />

## Terminal Settings Note
Before launching the script, please make sure your terminal window is scaled up to at least **80 columns by 25 rows** so the boundaries layout, score tracker, and retro frame buffer display correctly without text wrapping.
