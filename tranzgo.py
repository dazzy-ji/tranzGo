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
