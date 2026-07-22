def display_trip(trip, mode="bus"):
    """Display one trip: the journey, fare, and travel time."""
    print(f"\n    Trip: {trip['from']} -> {trip['to']}")
    print(f"    By {mode} -> Fare: {mode_fare(trip, mode)} RWF | "
          f"Estimated time: {mode_time(trip, mode)} min")

