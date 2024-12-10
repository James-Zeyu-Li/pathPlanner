# -*- coding: utf-8 -*-

# controller.py
import json
from pathlib import Path

# Use relative imports
from .path_planner_package.path_planner import PathPlanner
from .charging_strategy_optimizer.charging_strategy_optimizer import (
    load_car,
    load_path_planner,
    optimize_charging_strategy,
    traditional_strategy,
)

DATA_DIR = Path(__file__).resolve().parent / "data"
NODES_FILE = DATA_DIR / "nodes.json"
GRAPH_FILE = DATA_DIR / "graph.json"
CARS_FILE = DATA_DIR / "Cars.json"


def load_data(nodes_file, graph_file):
    """Load nodes and graph data from JSON files."""
    with open(nodes_file, 'r') as f:
        nodes = json.load(f)
    with open(graph_file, 'r') as f:
        graph = json.load(f)
    return nodes, graph


def initialize_planner(nodes, graph):
    """Initialize the PathPlanner object."""
    return PathPlanner(nodes=nodes, graph=graph)


def find_path(planner, start_city, end_city):
    """Find the shortest path between start_city and end_city."""
    if start_city not in planner.graph or end_city not in planner.graph:
        raise ValueError(
            f"Error: '{start_city}' or '{end_city}' not found in the graph."
        )
    return planner.find_shortest_path(start_city, end_city)


def prepare_segments(shortest_path, graph):
    """Extract segment distances from the shortest path."""
    segment_distances = []
    for i in range(len(shortest_path) - 1):
        start = shortest_path[i]
        end = shortest_path[i + 1]
        distance = graph[start][end]
        segment_distances.append((start, end, distance))
    return segment_distances


def load_vehicle_params(car_file, car_type):
    """Load vehicle parameters for the given car type."""
    return load_car(car_file, car_type)


def optimize_strategy(segment_distances, vehicle_params):
    """Optimize charging strategy for the given segments and vehicle parameters."""
    charging_stations = load_path_planner(segment_distances)
    optimal = optimize_charging_strategy(
        charging_stations, vehicle_params, vehicle_params['charging_curve'])
    traditional = traditional_strategy(
        charging_stations, vehicle_params, vehicle_params['charging_curve'])
    return optimal, traditional
