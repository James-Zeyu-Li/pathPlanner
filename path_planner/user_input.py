"""
This file parses user input into a readable format for the path_planner.py file.
"""
from path_planner import PathPlanner


def select_valid_city(planner: PathPlanner, cities: list, prompt: str) -> str:
    """
    Display available cities for selection and return the user's choice.

    Args:
        planner (PathPlanner): The PathPlanner instance.
        cities (list): A list of valid city names to choose from.
        prompt (str): Prompt message for the user.

    Returns:
        str: The selected city name.
    """
    while True:
        print("\nAvailable cities:")
        for i, city in enumerate(cities, 1):
            print(f"{i}: {city}")

        try:
            selection = int(input(f"\n{prompt} (Enter number): ").strip())
            if 1 <= selection <= len(cities):
                return cities[selection - 1]
            else:
                print(f"Invalid choice. Please select a number between 1 and {len(cities)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def main():
    """
    Main program to find the shortest and alternative paths between cities.
    """
    planner = PathPlanner()

    try:
        # Filter cities to include only those with a 'city' type
        label_cities = [
            city for city, details in planner.nodes.items()
            if details.get("type") == "city"
        ]

        # Handle case where no cities are available
        if not label_cities:
            print("No cities available. Please check your data.")
            return

        # Display available cities
        print("\nAvailable cities:", ", ".join(label_cities))

        # Select start and end cities
        start = select_valid_city(planner, label_cities, "Select start city")
        end = select_valid_city(planner, label_cities, "Select destination city")

        # Ensure start and destination are different
        if start == end:
            print("Start and destination cities cannot be the same.")
            return

        # Find the shortest path
        path, distance = planner.find_shortest_path(start, end)
        if not path:
            print(f"\nNo path found between {start} and {end}.")
            return

        print(f"\nBest path from {start} to {end}:")
        print(f"Route: {' -> '.join(path)}")
        print(f"Distance: {distance:.2f}")

        # Ask user for an alternative path
        if input("\nFind an alternative path? (y/n): ").lower().strip() == 'y':
            existing_paths = [(path, distance)]
            result = planner.find_alternative_path_with_penalty(
                start, end, existing_paths, penalty_factor=2.0
            )

            if not result:
                print("No alternative path found.")
            else:
                alt_path, _, actual_dist = result
                print(f"\nAlternative path:")
                print(f"Route: {' -> '.join(alt_path)}")
                print(f"Distance: {actual_dist:.2f}")

    except ValueError as e:
        print(f"\nError: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by the user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
