#!/usr/bin/env python3

# Section 1: Imports
import difflib

from db_config import connection

# How each means of transport changes the bus fare and time.
# For example a motorbike costs 2.5x the bus fare but takes 0.5x the time.
MODES = {
    "bus":       {"fare": 1.0, "time": 1.0},
    "motorbike": {"fare": 2.5, "time": 0.5},
    "car":       {"fare": 4.0, "time": 0.7},
}
