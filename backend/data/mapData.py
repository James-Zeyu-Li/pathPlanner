import random
import math
import networkx as nx
import matplotlib.pyplot as plt
import json
import os


def calculate_distance(loc1, loc2):
    return round(
        math.sqrt((loc2[0] - loc1[0]) ** 2 + (loc2[1] - loc1[1]) ** 2), 2
    )


def create_custom_structure():
    """
    Create a custom graph structure with cities and charging stations.
    """
    nodes = {
        "City1": {"type": "city", "location": (0, 200)},
        "City2": {"type": "city", "location": (350, 1000)},
        "City3": {"type": "city", "location": (950, 900)},
        "City4": {"type": "city", "location": (1000, 150)},
        "City5": {"type": "city", "location": (550, 0)},
    }
    graph = {}

    # Define connections between cities
    connections = {
        "City1": ["City2", "City4", "City5"],
        "City2": ["City1", "City3", "City4", "City5"],
        "City3": ["City2", "City4", "City5"],
        "City4": ["City1", "City2", "City3", "City5"],
        "City5": ["City1", "City2", "City3", "City4"],
    }

    # Generate charging stations between cities
    processed_paths = set()
    station_id = 1

    for city, neighbors in connections.items():
        for neighbor in neighbors:
            # Skip processed paths (undirected graph)
            if (city, neighbor) in processed_paths or \
               (neighbor, city) in processed_paths:
                continue

            processed_paths.add((city, neighbor))

            city_loc = nodes[city]["location"]
            neighbor_loc = nodes[neighbor]["location"]

            # Create charging stations along the path
            num_stations = random.randint(5, 8)
            station_nodes = []
            t_values = sorted(random.uniform(0.1, 1)
                              for _ in range(num_stations))

            for t in t_values:
                station_location = (
                    round(city_loc[0] + t *
                          (neighbor_loc[0] - city_loc[0]), 2),
                    round(city_loc[1] + t * (neighbor_loc[1] - city_loc[1]), 2)
                )
                station_name = f"Station{station_id}"
                nodes[station_name] = {
                    "type": "station", "location": station_location}
                station_nodes.append(station_name)
                station_id += 1

            # Connect charging stations and cities
            prev_node = city
            for station in station_nodes:
                dist = calculate_distance(
                    nodes[prev_node]["location"], nodes[station]["location"])
                graph.setdefault(prev_node, {})[station] = dist
                graph.setdefault(station, {})[prev_node] = dist
                prev_node = station

            # Connect last station to the destination city
            final_dist = calculate_distance(
                nodes[prev_node]["location"], neighbor_loc)
            graph.setdefault(prev_node, {})[neighbor] = final_dist
            graph.setdefault(neighbor, {})[prev_node] = final_dist

    return nodes, graph


def visualize_custom_graph(graph, nodes, save_path=None):
    """
    Visualize the graph with cities and charging stations.
    """
    G = nx.Graph()

    # Add nodes and edges to the graph
    for node, edges in graph.items():
        for neighbor, distance in edges.items():
            G.add_edge(node, neighbor, weight=distance)

    # Set node positions and colors
    pos = {node: nodes[node]["location"] for node in G.nodes}
    colors = ['red' if nodes[node]["type"] ==
              "city" else 'blue' for node in G.nodes]
    labels = {node: node for node in G.nodes}

    # Collect edge labels for distances
    edge_labels = {(u, v): f"{d:.2f}" for u, v, d in G.edges(data="weight")}

    # Draw the graph
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels,
            node_size=700, node_color=colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Save the graph image
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, format="png", dpi=300)
        print(f"Graph saved to {save_path}")

    plt.show()


def save_to_file(data, filepath):
    """
    Save data to a JSON file.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Failed to save data to {filepath}: {e}")


def load_from_file(filepath):
    """
    Load data from a JSON file.
    """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load data from {filepath}: {e}")
        return None


if __name__ == "__main__":
    # Create the custom graph structure
    nodes, graph = create_custom_structure()

    # Define file paths
    nodes_file = "backend/data/nodes.json"
    graph_file = "backend/data/graph.json"
    image_file = "backend/data/graph_visualization.png"

    # Save data to JSON files
    save_to_file(nodes, nodes_file)
    save_to_file(graph, graph_file)

    # Visualize and save the graph
    visualize_custom_graph(graph, nodes, save_path=image_file)

    # Verify data loading
    loaded_nodes = load_from_file(nodes_file)
    loaded_graph = load_from_file(graph_file)
    print("\nLoaded Nodes:", loaded_nodes)
    print("\nLoaded Graph:", loaded_graph)
