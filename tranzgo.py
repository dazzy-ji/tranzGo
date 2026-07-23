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

# Section 2: Trip Class
class Trip:
    """A single trip between two places."""

    def __init__(self, origin, destination, base_fare, travel_time_min):
        self.origin = origin
        self.destination = destination
        self.base_fare = base_fare              # bus fare in RWF
        self.travel_time_min = travel_time_min  # bus time in minutes

    def fare(self, mode):
        """Fare for this trip using the chosen means of transport."""
        return round(self.base_fare * MODES[mode]["fare"])

    def time(self, mode):
        """Travel time for this trip using the chosen means of transport."""
        return round(self.travel_time_min * MODES[mode]["time"])
