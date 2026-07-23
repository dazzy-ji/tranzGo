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
