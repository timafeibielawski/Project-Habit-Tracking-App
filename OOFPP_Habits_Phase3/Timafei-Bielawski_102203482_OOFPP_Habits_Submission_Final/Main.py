import os
import subprocess
import sys
import time
from datetime import timedelta
import shutil  # To fetch terminal width dynamically

# --------------------------------------------
# Function to auto-install required packages
# --------------------------------------------
def ensure_package(pkg):
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# Ensure necessary libraries are installed
ensure_package("colorama")
ensure_package("prettytable")

import colorama
from colorama import Fore, Style
from HabitsTrackerApp import Tracker

# --------------------------------------------
# Color Setup
# --------------------------------------------
colorama.init()
MainColor, Highlight, ResetColor = Fore.CYAN, Fore.YELLOW, Style.RESET_ALL

# --------------------------------------------
# Clears the terminal screen
# --------------------------------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --------------------------------------------
# Displays user instructions and available commands
# --------------------------------------------
def show_commands():
    print(f"{Highlight}Available Commands:{ResetColor}")
    print(f"{MainColor} add <habit>     {ResetColor}→ Create a new habit")
    print(f"{MainColor} done <habit>    {ResetColor}→ Mark this habit as done for the current cycle")
    print(f"{MainColor} remove <habit>  {ResetColor}→ Delete a habit")
    print(f"{MainColor} show            {ResetColor}→ View habit data")
    print(f"{MainColor} clock           {ResetColor}→ Show live countdowns")
    print(f"{MainColor} h               {ResetColor}→ Help menu")
    print(f"{MainColor} q               {ResetColor}→ Quit")

# --------------------------------------------
# Initialize the habit tracker instance
# --------------------------------------------
habits = Tracker()

# --------------------------------------------
# Main application loop
# --------------------------------------------
while True:
    clear_screen()
    print(f"{Highlight}Progress is progress – no matter how small!{ResetColor}")
    print(f"{MainColor}Welcome to your Habit Dashboard 🧠{ResetColor}\n")

    # Auto-resize the table to match terminal width
    columns, _ = shutil.get_terminal_size()
    habits.habits_table(max_width=columns)

    show_commands()
    user_input = input(f"\n{MainColor}Command: {ResetColor}").strip().lower()
    if not user_input:
        continue

    parts = user_input.split()
    command = parts[0]
    param = " ".join(parts[1:]) if len(parts) > 1 else ""

    # ---------------- ADD HABIT ----------------
    if command == "add":
        if not param:
            continue
        goal = input(f"{MainColor}Goal: {ResetColor}")
        while True:
            cycle_type = input(f"{MainColor}Cycle unit - (d)ays or (w)eeks? {ResetColor}").lower()
            if cycle_type in ["d", "w"]: break
            print("Please enter 'd' or 'w'")
        while True:
            length = input(f"{MainColor}Cycle length in {'days' if cycle_type == 'd' else 'weeks'}: {ResetColor}")
            if length.isdigit():
                length = int(length)
                break
            print("Enter a valid number.")
        while True:
            freq = input(f"{MainColor}How many times per cycle (number): {ResetColor}")
            if freq.isdigit():
                freq = int(freq)
                break
            print("Enter a valid number.")
        note = input(f"{MainColor}Optional note (e.g. 'before bed'): {ResetColor}")
        habits.add_habit(param, goal, length, freq, note, cycle_type)

    # ---------------- MARK AS DONE ----------------
    elif command == "done":
        if param:
            habits.all_habits_list(True)
            habits.check_off_habit(param)

    # ---------------- REMOVE HABIT ----------------
    elif command == "remove":
        if param:
            habits.all_habits_list(True)
            habits.remove_habit(param)

        # ---------------- SHOW ANALYTICS ----------------
    elif command == "show":
        while True:
            clear_screen()
            print(f"{Highlight}📊 Habit Analytics Dashboard{ResetColor}\n")
            print(f"{MainColor} 1 {ResetColor}- All tracked habits")
            print(f"{MainColor} 2 {ResetColor}- Daily habits only")
            print(f"{MainColor} 3 {ResetColor}- Weekly habits only")
            print(f"{MainColor} 4 {ResetColor}- Longest overall streak")
            print(f"{MainColor} 5 {ResetColor}- Best streak by habit")
            print(f"{MainColor} 6 {ResetColor}- Reprint habit table")
            print(f"{MainColor} 7 {ResetColor}- Back to main menu")

            opt = input(f"\n{MainColor}Choose: {ResetColor}").strip()

            if opt == "1":
                habits.all_habits_list(True)
            elif opt == "2":
                if not habits.all_daily_habits_list(True):
                    print("⚠️ No daily habits found.")
            elif opt == "3":
                if not habits.all_weekly_habits_list(True):
                    print("⚠️ No weekly habits found.")
            elif opt == "4":
                habits.longest_streak_of_all_habits(True)
            elif opt == "5":
                habits.all_habits_list(True)
                name = input(f"{MainColor}Habit name: {ResetColor}")
                habits.longest_streak_of_habit(name, True)
            elif opt == "6":
                columns, _ = shutil.get_terminal_size()
                habits.habits_table(max_width=columns)
            elif opt == "7":
                break
            else:
                print(f"{Fore.RED}Invalid input. Try again.{ResetColor}")
                continue

            input(f"\n{Highlight}Press Enter to continue...{ResetColor}")

    # ---------------- CLOCK COUNTDOWN ----------------
    elif command == "clock":
        for _ in range(10):  # Simulate for 10 seconds
            clear_screen()
            print("\n📅 Live Countdown for Habit Cycles:\n")
            for name, info in habits.data.items():
                start = info.get("Start_Time", time.time())
                cycle_type = info.get("Cycle_Type", "days")
                length = info.get("Time_Frame", 1)
                seconds = length * 7 * 86400 if cycle_type == "weeks" else length * 86400
                remaining = max(0, int(start + seconds - time.time()))
                print(f"⏳ {name}: {str(timedelta(seconds=remaining))} left")
            time.sleep(1)

    # ---------------- HELP ----------------
    elif command == "h":
        show_commands()

    # ---------------- QUIT ----------------
    elif command == "q":
        print(f"{MainColor}Thanks for using the Habit Tracker. Stay consistent!{ResetColor}")
        break

    # ---------------- UNKNOWN ----------------
    else:
        print(f"{Fore.RED}Unknown command. Type 'h' for help.{ResetColor}")
