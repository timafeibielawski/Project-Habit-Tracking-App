# Project Habit Tracking App

This is a terminal-based habit tracking application written in Python. It allows users to manage, track, and analyze both daily and weekly habits with a clean and responsive command-line interface. The app provides features such as streak tracking, countdown timers, and a dynamic tabular display.

---

## Features

- Add, check off, and remove custom habits
- Support for daily or weekly tracking cycles
- Countdown timers for each habit's current cycle
- Current and best streak tracking
- Tabular display of all habits, adjusted to terminal width
- User-friendly interface
- Auto-refresh after each action for smooth interaction
- Automatically restores a placeholder habit when the list is empty

---

## Installation

**Requirements:** Python 3.7 or higher

1. Clone the repository

2. Run the main application:
   ```bash
   python Main.py
   ```

The app will automatically install necessary libraries such as:
- `prettytable`
- `colorama`

A `Data.json` file will be created on first run to store habit data.

---

## Usage

After launching, the app will display your current habits and a command list.

### Available Commands

| Command            | Description                                         |
|--------------------|-----------------------------------------------------|
| `add <habit>`      | Create a new habit (you'll be prompted for details) |
| `done <habit>`     | Mark a habit as completed for the current cycle     |
| `remove <habit>`   | Delete a habit from tracking                        |
| `show`             | Access analytics and habit display options          |
| `clock`            | Show live countdown for each habit cycle            |
| `h`                | Show help menu with available commands              |
| `q`                | Quit the application                                |

---

## Data Storage

All habit information is saved in a local `Data.json` file. It includes fields like:
- `Goal`
- `Time_Frame` (cycle length)
- `TargetPerPeriod` (how often it should be done)
- `Cycle_Type` (days or weeks)
- `Counter`, `BestStreak`, `Start_Time`, `Last_Checked`, and optional notes

---
