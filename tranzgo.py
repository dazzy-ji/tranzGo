# Section 4: User Interface Class
class TranzGoApp:
    """The menu-driven program the user interacts with."""

    def __init__(self, database):
        self.database = database
        self.places = database.all_places()   # used for typing help