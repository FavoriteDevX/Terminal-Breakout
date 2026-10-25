# Terminal Breakout Game

A fully playable, retro-style Breakout game built in Python that runs entirely inside your computer terminal. 

No external package managers like `npm`, `pip`, or `node` required! It uses Python's standard built-in `curses` module.

## How to Play

1. **Clone or Copy the code:** Save the script as `breakout.py`.
2. **Run the game:** Open your terminal and run:
   ```bash
   python breakout.py
   ```
   *(On some systems, you might need to use `python3 breakout.py`)*

## Controls

* **Move Left:** `A` or `Left Arrow Key`
* **Move Right:** `D` or `Right Arrow Key`
* **Restart Game:** `R` (When Game Over or Victory)
* **Quit Game:** `Q`

## Windows Note
If you are running this on **Windows**, the native terminal does not include the `curses` module by default. To make it work seamlessly without installing standard pip dependencies, run it inside the **Git Bash** terminal or **WSL (Windows Subsystem for Linux)**.
