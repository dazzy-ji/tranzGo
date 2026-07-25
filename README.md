# TranzGo

TranzGo is a menu-driven Python application that helps users find trips between places in Rwanda, compare fares and travel times across different means of transport (bus, motorbike, car), and calculate total fares for a group of passengers. Trip data is stored in a MySQL database.

## Features

1. **Find a Trip** — Enter a starting point and destination to see the fare and travel time by your chosen means of transport.
2. **Browse** — View all trips in the database, or view every known place (A–Z).
3. **Fare Calculator** — Get a full fare summary (per-person fare, travel time, and total cost) for a group of passengers.

## How it Works

- Trip data (origin, destination, base bus fare, and bus travel time) is stored in a MySQL `trips` table.
- Fares and times for other means of transport are calculated by scaling the base bus fare/time using multipliers defined in `MODES`:

| Mode       | Fare multiplier | Time multiplier |
|------------|------------------|------------------|
| Bus        | 1.0x             | 1.0x             |
| Motorbike  | 2.5x             | 0.5x             |
| Car        | 4.0x             | 0.7x             |

- Place names are matched without case sensitivity, and typos are caught using `difflib`'s close-match suggestions.

## Requirements

- Python 3.8+
- A MySQL server with a `trips` table containing: `origin`, `destination`, `base_fare`, `travel_time_min`

## Setup

1. Clone the repository:
```bash
   git clone <repo-url>
   cd tranzgo
```

2. Install the MySQL driver:
```bash
   pip install mysql-connector-python
```

3. Create your own `db_config.py` (see `db_config.py.example`) with your database credentials.

4. Run the app:
```bash
   python tranzgo.py
```

## Usage

On launch, choose from:
```
>>> 1. Find a trip   2. Browse   3. Fare calculator   4. Exit
```
