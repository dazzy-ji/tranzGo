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
        return trips