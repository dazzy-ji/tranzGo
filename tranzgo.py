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

# Section 3: Database Class
class TripDatabase:
    def __init__(self, connection):
        self.connection = connection

    def all_places(self):
        #Retrieve all places from the database, ASC order
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT origin FROM trips "
            "UNION SELECT destination FROM trips "
            "ORDER BY 1"
        )
        places = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return places

    def lookup(self, start, destination):
        #Retrieve trips from the database based on start and destination
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT base_fare, travel_time_min FROM trips "
            "WHERE (origin = %s AND destination = %s) " 
            "OR (origin = %s AND destination = %s) "
            "LIMIT 1",
            (start, destination, destination, start),
        )
        row = cursor.fetchall()
        cursor.close()

        if row is None:
            return None
        return Trip(start, destination, row[0], row[1])

    def all_trips(self):
        #Retrieve all trips from the database
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT origin, destination, base_fare, travel_time_min " 
            "FROM trips ORDER BY origin, destination"
        )
        trips = [Trip(*row) for row in cursor.fetchall()]
        cursor.close()
        return trips# Section 4: User Interface Class
class TranzGoApp:
    """The menu-driven program the user interacts with."""

    def __init__(self, database):
        self.database = database
        self.places = database.all_places()   # used for typing help

    # ----- asking the user for input -----

    def ask_place(self, prompt):
        """Ask for a place name until the user gives a valid one."""
        while True:
            name = input(prompt).strip()
            if not name:
                print("    Please type a place name.")
                continue

            # Match ignoring capital letters (kimironko == Kimironko).
            for place in self.places:
                if place.lower() == name.lower():
                    return place

            # Not found - suggest the closest spelling (typo helper).
            close = difflib.get_close_matches(
                name, self.places, n=1, cutoff=0.6)
            if close:
                answer = input(
                    f"    Did you mean '{close[0]}'? (y/n): ").strip().lower()
                if answer in ("y", "yes"):
                    return close[0]

            print(f"    '{name}' is not a known place. "
                  "Pick option 2 to see all places.")

    def ask_mode(self):
        """Ask for a means of transport until the user gives a valid one."""
        options = ", ".join(MODES)
        while True:
            mode = input(f">>> Means of transport ({options}): ").strip().lower()
            if mode in MODES:
                return mode
            print(f"    Please choose one of: {options}.")

    def ask_count(self):
        """Ask for the number of passengers (a positive whole number)."""
        while True:
            answer = input(">>> Number of passengers: ").strip()
            if answer.isdigit() and int(answer) > 0:
                return int(answer)
            print("    Please enter a whole number of 1 or more.")

    
            
