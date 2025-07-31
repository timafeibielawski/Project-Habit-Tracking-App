import os
import time
import json
import shutil
from prettytable import PrettyTable

class Tracker:
    def __init__(self):
        self.filename = "Data.json"
        self.load_data()

    # Load JSON data or initialize default
    def load_data(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)
        with open(self.filename, "r") as f:
            self.data = json.load(f)
        if not self.data:
            self.insert_default()

    # Save current habit data to JSON
    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    # Insert a placeholder habit when starting fresh
    def insert_default(self):
        self.data["DefaultHabit"] = {
            "Goal": "",
            "Time_Frame": 1,
            "TargetPerPeriod": 1,
            "FrequencyNote": "",
            "Cycle_Type": "days",
            "Counter": 0,
            "Start_Time": time.time(),
            "Last_Checked": None,
            "BestStreak": 0
        }
        self.save_data()

    # Display all habits in a dynamic-width table
    def habits_table(self, max_width=None):
        if not self.data:
            print("You haven't added any habits yet.")
            return

        table = PrettyTable()
        table.field_names = [
            "Habit", "Goal", "Times / Cycle", "Cycle (days/weeks)",
            "Note", "Top Streak", "Current"
        ]

        for habit, info in self.data.items():
            duration = info.get("Time_Frame", 0)
            unit = info.get("Cycle_Type", "days")
            table.add_row([
                habit,
                info.get("Goal", ""),
                info.get("TargetPerPeriod", 0),
                f"{duration} {unit}",
                info.get("FrequencyNote", ""),
                info.get("BestStreak", 0),
                info.get("Counter", 0)
            ])

        # Fit to screen width if needed
        if max_width:
            table.max_width = max_width
        else:
            columns, _ = shutil.get_terminal_size()
            table.max_width = columns

        print(table)

    # Add a new habit (or replace placeholder)
    def add_habit(self, name, goal, time_frame, target, note="", cycle_type="days"):
        if len(self.data) == 1 and "default" in list(self.data.keys())[0].lower():
            self.data.clear()

        if name in self.data:
            print(f"The habit '{name}' already exists.")
            return

        now = time.time()
        self.data[name] = {
            "Goal": goal,
            "Time_Frame": time_frame,
            "TargetPerPeriod": target,
            "FrequencyNote": note,
            "Cycle_Type": "weeks" if cycle_type == "w" else "days",
            "Counter": 0,
            "Start_Time": now,
            "Last_Checked": None,
            "BestStreak": 0
        }
        self.save_data()
        print(f"New habit '{name}' added!")

    # Mark a habit as completed
    def check_off_habit(self, name):
        if name not in self.data:
            print(f"Habit '{name}' doesn't exist.")
            return

        now = time.time()
        habit = self.data[name]
        length = habit.get("Time_Frame", 1)
        unit = habit.get("Cycle_Type", "days")
        cycle_seconds = length * (7 if unit == "weeks" else 1) * 86400
        last_checked = habit.get("Last_Checked")

        if last_checked and now - last_checked < cycle_seconds:
            habit["Counter"] += 1
        else:
            habit["Counter"] = 1
            habit["Start_Time"] = now

        habit["Last_Checked"] = now

        if habit["Counter"] > habit["BestStreak"]:
            habit["BestStreak"] = habit["Counter"]

        self.save_data()
        print(f"✅ You’ve logged progress for '{name}'.")

    # Remove a habit from the tracker
    def remove_habit(self, name):
        if name not in self.data:
            print(f"Habit '{name}' not found.")
            return

        del self.data[name]
        print(f"'{name}' has been removed.")

        if not self.data:
            self.insert_default()
            print("All habits removed. Default placeholder added.")

        self.save_data()

    # Print a list of all habit names
    def all_habits_list(self, show=False):
        if show:
            print("📋 Current Habits:")
            for habit in self.data:
                print(f" - {habit}")

    # Print daily habits only; return True if found
    def all_daily_habits_list(self, show=False):
        found = False
        if show:
            print("📆 Daily Habits:")
            for name, info in self.data.items():
                if info.get("Cycle_Type") == "days":
                    print(f" - {name}")
                    found = True
        return found

    # Print weekly habits only; return True if found
    def all_weekly_habits_list(self, show=False):
        found = False
        if show:
            print("🗓️ Weekly Habits:")
            for name, info in self.data.items():
                if info.get("Cycle_Type") == "weeks":
                    print(f" - {name}")
                    found = True
        return found

    # Find and display the longest streak among all habits
    def longest_streak_of_all_habits(self, show=False):
        if not self.data:
            print("No habits to evaluate.")
            return

        best = max(self.data.items(), key=lambda item: item[1].get("BestStreak", 0))
        if show:
            print(f"🏆 Longest overall streak is '{best[0]}' with {best[1]['BestStreak']}.")

    # Display best streak for a specific habit
    def longest_streak_of_habit(self, name, show=False):
        if name not in self.data:
            print(f"Habit '{name}' does not exist.")
            return
        if show:
            print(f"🔥 Best streak for '{name}': {self.data[name]['BestStreak']}")
