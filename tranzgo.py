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
        row = cursor.fetchone()
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
        return trips

# Section 4: User Interface Class
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

    def find_trip(self):
        """Feature 1: find a trip and show its fare and time."""
        print("\n--- Find a Trip ---")
        start = self.ask_place(">>> Enter your starting point: ")
        destination = self.ask_place(">>> Enter your destination: ")

        if start == destination:
            print("    Start and destination are the same place!")
            return

        mode = self.ask_mode()
        trip = self.database.lookup(start, destination)

        if trip is None:
            print(f"\n     Sorry, there is no direct trip from "
                  f"{start} to {destination}.")
        else:
            print(f"\n     Trip: {trip.origin} -> {trip.destination}")
            print(f"     By {mode} -> Fare: {trip.fare(mode)} RWF | "
                  f"Time: {trip.time(mode)} min")

    def browse(self):
        """Feature 2: list all trips, or all places."""
        print("\n--- Browse ---")
        print(">>> 1. View all trips     2. View all places (A-Z)")
        choice = input(">>> Choose an option: ").strip()

        if choice == "1":
            trips = self.database.all_trips()
            print(f"\n     All trips ({len(trips)} total, both directions):")
            for trip in trips:
                print(f"     - {trip.origin} <-> {trip.destination} "
                      f"({trip.base_fare} RWF by bus, "
                      f"{trip.travel_time_min} min)")
        elif choice == "2":
            print(f"\n     All places ({len(self.places)} total):")
            for place in self.places:
                print(f"     - {place}")
        else:
            print("     Invalid option. Returning to main menu.")

    def fare_calculator(self):
        """Feature 3: total fare for a trip and a group of passengers."""
        print("\n--- Fare Calculator ---")
        start = self.ask_place(">>> Enter your starting point: ")
        destination = self.ask_place(">>> Enter your destination: ")

        trip = self.database.lookup(start, destination)
        if trip is None:
            print(f"\n     Sorry, there is no direct trip from "
                  f"{start} to {destination}.")
            return

        mode = self.ask_mode()
        count = self.ask_count()
        total = trip.fare(mode) * count

        print("\n     ---- Fare Summary ----")
        print(f"     Trip: {trip.origin} -> {trip.destination}")
        print(f"     Means of transport: {mode}")
        print(f"     Fare per person: {trip.fare(mode)} RWF")
        print(f"     Passengers: {count}")
        print(f"     Time: {trip.time(mode)} min")
        print(f"     TOTAL: {total} RWF")
        print("     ----------------------")

 # ----- the main menu loop -----
    def run(self):
        """Show the welcome message, then loop over the menu until exit."""
        print("=" * 60)
        print("        Welcome to TranzGo - your public transport guide")
        print("=" * 60)

        while True:
            print("\n" + "-" * 60)
            print(">>> 1. Find a trip   2. Browse   "
                  "3. Fare calculator   4. Exit")
            print("-" * 60)
            choice = input(">>> Choose an option (1-4): ").strip()

            if choice == "1":
                self.find_trip()
            elif choice == "2":
                self.browse()
            elif choice == "3":
                self.fare_calculator()
            elif choice == "4":
                print("\nThank you for using TranzGo. Safe travels!")
                break
            else:
                print("    Please enter 1, 2, 3 or 4.")


# ----- start the program -----

def main():
    database = TripDatabase(connection)
    app = TranzGoApp(database)
    try:
        app.run()
    finally:
        connection.close()


if __name__ == "__main__":
    main()    
