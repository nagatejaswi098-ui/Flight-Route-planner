from itertools import permutations

# Flight network
flights = {
    "Hyderabad": {
        "Mumbai": 4000,
        "Delhi": 6000
    },
    "Mumbai": {
        "Hyderabad": 4000,
        "Delhi": 3000,
        "Kolkata": 5000
    },
    "Delhi": {
        "Hyderabad": 6000,
        "Mumbai": 3000,
        "Kolkata": 4500
    },
    "Kolkata": {
        "Mumbai": 5000,
        "Delhi": 4500
    }
}


# ---------------- Dijkstra Algorithm ----------------
def dijkstra(flights, start, end):

    distances = {city: float("inf") for city in flights}
    previous = {city: None for city in flights}

    distances[start] = 0
    unvisited = list(flights.keys())

    while unvisited:

        current = min(
            unvisited,
            key=lambda city: distances[city]
        )

        unvisited.remove(current)

        if distances[current] == float("inf"):
            break

        for neighbor, cost in flights[current].items():

            new_cost = distances[current] + cost

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous[neighbor] = current

    # Create route
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    if path[0] != start:
        return None, None

    return path, distances[end]


# ---------------- Floyd-Warshall Algorithm ----------------
def floyd_warshall(flights):

    cities = list(flights.keys())

    distance = {}

    # Initial distances
    for city in cities:

        distance[city] = {}

        for other in cities:

            if city == other:
                distance[city][other] = 0

            else:
                distance[city][other] = flights[city].get(
                    other,
                    float("inf")
                )

    # Find shortest paths
    for middle in cities:

        for start in cities:

            for end in cities:

                new_cost = (
                    distance[start][middle]
                    + distance[middle][end]
                )

                if new_cost < distance[start][end]:
                    distance[start][end] = new_cost

    return distance


# ---------------- TSP Algorithm ----------------
def tsp(flights, start):

    cities = [city for city in flights if city != start]

    best_route = None
    min_cost = float("inf")

    for order in permutations(cities):

        route = [start] + list(order)

        cost = 0
        possible = True

        for i in range(len(route) - 1):

            current = route[i]
            next_city = route[i + 1]

            if next_city not in flights[current]:
                possible = False
                break

            cost += flights[current][next_city]

        if possible and cost < min_cost:

            min_cost = cost
            best_route = route

    return best_route, min_cost


# ---------------- Display Flights ----------------
def show_flights():

    print("\n========== FLIGHT NETWORK ==========")

    for city in flights:

        for destination, cost in flights[city].items():

            print(
                city,
                "->",
                destination,
                ": ₹",
                cost
            )


# ---------------- Main Menu ----------------
def main():

    while True:

        print("\n====================================")
        print("       FLIGHT ROUTE PLANNER")
        print("====================================")

        print("1. Find Minimum Cost Route")
        print("2. Show Floyd-Warshall Results")
        print("3. Find TSP Route")
        print("4. Show Flight Network")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        # Dijkstra
        if choice == "1":

            print("\nAvailable Cities:")

            for city in flights:
                print("-", city)

            start = input("\nEnter starting city: ")
            end = input("Enter destination city: ")

            if start not in flights or end not in flights:

                print("\nInvalid city!")

            elif start == end:

                print("\nStarting city and destination cannot be same.")

            else:

                path, cost = dijkstra(
                    flights,
                    start,
                    end
                )

                if path is None:

                    print("\nNo route available.")

                else:

                    print("\nShortest Route:")
                    print(" -> ".join(path))

                    print("Total Travel Cost: ₹", cost)

        # Floyd-Warshall
        elif choice == "2":

            result = floyd_warshall(flights)

            print("\n========== FLOYD-WARSHALL ==========")

            cities = list(flights.keys())

            for start in cities:

                print("\nFrom", start)

                for end in cities:

                    cost = result[start][end]

                    if cost == float("inf"):
                        print(end, ": No route")

                    else:
                        print(end, ": ₹", cost)

        # TSP
        elif choice == "3":

            print("\nAvailable Cities:")

            for city in flights:
                print("-", city)

            start = input("\nEnter starting city: ")

            if start not in flights:

                print("\nInvalid city!")

            else:

                route, cost = tsp(
                    flights,
                    start
                )

                if route is None:

                    print("\nNo possible TSP route.")

                else:

                    print("\nTSP Route:")
                    print(" -> ".join(route))

                    print("Total Travel Cost: ₹", cost)

        # Show flights
        elif choice == "4":

            show_flights()

        # Exit
        elif choice == "5":

            print("\nThank you for using Flight Route Planner!")

            break

        else:

            print("\nInvalid choice! Please try again.")


# Start program
if __name__ == "__main__":
    main()