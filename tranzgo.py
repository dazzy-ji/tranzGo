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

    
            
