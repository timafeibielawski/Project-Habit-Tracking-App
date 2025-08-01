# To run these tests, make sure pytest is installed:
# pip install pytest


import pytest
import os
import time
import json
from HabitsTrackerApp import Tracker

TEST_FILE = "test_data.json"

@pytest.fixture
def tracker():
    # Setup: Create a tracker with a test file
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    tr = Tracker()
    tr.filename = TEST_FILE
    tr.data = {}
    tr.save_data()
    return tr

def test_add_habit(tracker):
    tracker.add_habit("test_habit", "Test Goal", 7, 3, "every evening", "d")
    assert "test_habit" in tracker.data
    assert tracker.data["test_habit"]["Goal"] == "Test Goal"

def test_check_off_habit(tracker):
    tracker.add_habit("exercise", "Do 30 mins of exercise", 1, 1, "morning", "d")
    tracker.check_off_habit("exercise")
    habit = tracker.data["exercise"]
    assert habit["Counter"] == 1
    assert habit["BestStreak"] == 1

def test_check_off_habit_twice_same_cycle(tracker):
    tracker.add_habit("read", "Read a book", 1, 1, "", "d")
    tracker.check_off_habit("read")
    tracker.check_off_habit("read")
    assert tracker.data["read"]["Counter"] == 2
    assert tracker.data["read"]["BestStreak"] == 2

def test_remove_habit(tracker):
    tracker.add_habit("meditate", "Relax the mind", 1, 1, "", "d")
    tracker.remove_habit("meditate")
    assert "meditate" not in tracker.data

def test_longest_streak(tracker):
    tracker.add_habit("walk", "Take a walk", 1, 1, "", "d")
    for _ in range(3):
        tracker.check_off_habit("walk")
    longest = max(tracker.data.items(), key=lambda item: item[1].get("BestStreak", 0))
    assert longest[0] == "walk"
    assert longest[1]["BestStreak"] == 3
