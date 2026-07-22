
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
