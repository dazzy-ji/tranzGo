def display_trip(trip, mode="bus"):

    print(f"\n    Trip: {trip['from']} -> {trip['to']}")
    print(f"    By {mode} -> Fare: {mode_fare(trip, mode)} RWF | "
          f"Estimated time: {mode_time(trip, mode)} min")
    def find_trip_menu(conn, all_places):
    print("\n--- Find a Trip ---")

    start = prompt_for_place(">>> Enter your starting point: ", all_places)
    destination = prompt_for_place(">>> Enter your destination: ", all_places)

    if start == destination:
        print("    Start and destination are the same place. No trip needed!")
        return

    mode = choose_mode()

    trip = fetch_trip(conn, start, destination)
    if trip:
        display_trip(trip, mode)
    else:
        print(f"\n    Sorry, there is no direct trip from "
              f"{start} to {destination}.")

