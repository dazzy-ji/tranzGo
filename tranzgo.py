
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
            print(f"\n    Sorry, there is no direct trip from "
                  f"{start} to {destination}.")
        else:
            print(f"\n    Trip: {trip.origin} -> {trip.destination}")
            print(f"    By {mode} -> Fare: {trip.fare(mode)} RWF | "
                  f"Time: {trip.time(mode)} min")

    def browse(self):
        """Feature 2: list all trips, or all places."""
        print("\n--- Browse ---")
        print(">>> 1. View all trips   2. View all places (A-Z)")
        choice = input(">>> Choose an option: ").strip()

        if choice == "1":
            trips = self.database.all_trips()
            print(f"\n    All trips ({len(trips)} total, both directions):")
            for trip in trips:
                print(f"    - {trip.origin} <-> {trip.destination}  "
                      f"({trip.base_fare} RWF by bus, "
                      f"{trip.travel_time_min} min)")
        elif choice == "2":
            print(f"\n    All places ({len(self.places)} total):")
            for place in self.places:
                print(f"    - {place}")
        else:
            print("    Invalid option. Returning to main menu.")

    def fare_calculator(self):
        """Feature 3: total fare for a trip and a group of passengers."""
        print("\n--- Fare Calculator ---")
        start = self.ask_place(">>> Enter your starting point: ")
        destination = self.ask_place(">>> Enter your destination: ")

        trip = self.database.lookup(start, destination)
        if trip is None:
            print(f"    Sorry, there is no direct trip from "
                  f"{start} to {destination}.")
            return

        mode = self.ask_mode()
        count = self.ask_count()
        total = trip.fare(mode) * count

        print("\n    ---- Fare Summary ----")
        print(f"    Trip: {trip.origin} -> {trip.destination}")
        print(f"    Means of transport: {mode}")
        print(f"    Fare per person: {trip.fare(mode)} RWF")
        print(f"    Passengers: {count}")
        print(f"    Time: {trip.time(mode)} min")
        print(f"    TOTAL: {total} RWF")
        print("    ----------------------")
