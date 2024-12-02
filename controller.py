# -*- coding: utf-8 -*-

# controller.py

import json
from path_planner import PathPlanner
from charging_strategy_optimizer import load_car, load_path_planner, optimize_charging_strategy, traditional_strategy

def main():
    # Initialize the PathPlanner object with loaded nodes and graph data
    nodes_file = "data/nodes.json"
    graph_file = "data/graph.json"
    
    # Load nodes and graph from JSON files
    try:
        with open(nodes_file, 'r') as f:
            nodes = json.load(f)
        with open(graph_file, 'r') as f:
            graph = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return
    
    # Initialize path planner with nodes and graph
    planner = PathPlanner(nodes=nodes, graph=graph)
    
    # Define start and end nodes for the path
    start_city = "City1"
    end_city = "City3"
    
    # Check if the nodes exist in the graph
    if start_city not in planner.graph or end_city not in planner.graph:
        print(f"Error: One or both of the cities '{start_city}' or '{end_city}' are not found in the graph.")
        return
    
    # Use path planner to find the shortest path
    try:
        shortest_path, total_distance, segment_distances = planner.find_shortest_path(start_city, end_city)
    except KeyError as e:
        print(f"Error finding shortest path: {e}")
        return
    
    # Print the shortest path
    print("Shortest Path:", shortest_path)
    print("Total Distance:", total_distance)
    
    # Get segment distances for optimizer input
    segment_distances = []
    for i in range(len(shortest_path) - 1):
        start = shortest_path[i]
        end = shortest_path[i + 1]
        distance = graph[start][end]
        segment_distances.append((start, end, distance))
    
    # Load car parameters
    car_file = "data/Cars.json"
    car_type = "Semi"
    try:
        vehicle_params = load_car(car_file, car_type)
    except ValueError as e:
        print(f"Error loading car data: {e}")
        return
    
    # Convert path segments to charging stations
    charging_stations = load_path_planner(segment_distances)
    
    # Optimize charging strategy
    try:
        optimal_strategy, total_time_optimal, total_charging_time_optimal, total_driving_time_optimal = optimize_charging_strategy(charging_stations, vehicle_params, vehicle_params['charging_curve'])
    except ValueError as e:
        print(f"Error optimizing charging strategy: {e}")
        return
    
    # Print optimal charging strategy
    print("\nOptimal Charging Strategy:")
    for step in optimal_strategy:
        if step['charge_amount'] > 0:
            print(f"At {step['station']}, charged from {step['departure_soc'] - step['charge_amount']}% to {step['departure_soc']}%, charged {step['charge_amount']}%")

    print(f"Total Travel Time (Optimal): {total_time_optimal:.2f} hours")
    print(f"Total Charging Time (Optimal): {total_charging_time_optimal:.2f} hours")
    print(f"Total Driving Time (Optimal): {total_driving_time_optimal:.2f} hours")
    
    # Traditional charging strategy
    try:
        traditional_strategy_result, total_time_traditional, total_charging_time_traditional, total_driving_time_traditional = traditional_strategy(charging_stations, vehicle_params, vehicle_params['charging_curve'])
    except ValueError as e:
        print(f"Error with traditional charging strategy: {e}")
        return
    
    # Print traditional charging strategy
    print("\nTraditional Charging Strategy:")
    for step in traditional_strategy_result:
        print(f"At {step['station']}, charged from {step['departure_soc'] - step['charge_amount']}% to {step['departure_soc']}%, charged {step['charge_amount']}%")
    print(f"Total Travel Time (Traditional): {total_time_traditional:.2f} hours")
    print(f"Total Charging Time (Traditional): {total_charging_time_traditional:.2f} hours")
    print(f"Total Driving Time (Traditional): {total_driving_time_traditional:.2f} hours")

if __name__ == "__main__":
    main()
