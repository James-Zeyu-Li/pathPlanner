import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from path_planner import PathPlanner


# 文件路径配置
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
NODES_FILE = DATA_DIR / "nodes.json"
GRAPH_FILE = DATA_DIR / "graph.json"


def load_graph_data():
    """
    Load nodes and graph data from JSON files.
    """
    try:
        with open(NODES_FILE) as f:
            nodes = json.load(f)
        with open(GRAPH_FILE) as f:
            graph = json.load(f)
        return nodes, graph
    except FileNotFoundError:
        print("Error: Data files not found.")
        return None, None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in data files.")
        return None, None


def visualize_path(nodes, graph, path, alt_path=None, save_path=None):
    """
    Visualize the graph with the shortest path and alternative path highlighted.
    Node positions and labels are based on predefined locations from nodes.
    """
    G = nx.Graph()

    # Add all nodes and edges from the graph
    for node, edges in graph.items():
        for neighbor, weight in edges.items():
            G.add_edge(node, neighbor, weight=weight)

    # Extract edges for shortest and alternative paths
    path_edges = list(zip(path[:-1], path[1:])) if path else []
    alt_edges = list(zip(alt_path[:-1], alt_path[1:])) if alt_path else []

    # Collect all nodes involved in shortest and alternative paths
    highlighted_nodes = set()
    if path:
        highlighted_nodes.update(path)
    if alt_path:
        highlighted_nodes.update(alt_path)

    # Use actual positions from nodes' "location"
    pos = {node: (details["location"][0], details["location"][1])
           for node, details in nodes.items()}

    # Define node colors: highlighted nodes keep their type color, others are grey
    colors = [
        'red' if nodes[node]["type"] == "city" and node in highlighted_nodes
        else 'blue' if nodes[node]["type"] == "station" and node in highlighted_nodes
        else 'lightgrey'
        for node in G.nodes
    ]

    # Draw the graph with all edges in light grey for context
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color=colors,
            node_size=700, edge_color="lightgrey", font_size=10)

    # Highlight shortest path edges
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                               edge_color="green", width=2, label="Shortest Path")

    # Highlight alternative path edges
    if alt_edges:
        nx.draw_networkx_edges(G, pos, edgelist=alt_edges, edge_color="orange",
                               width=2, style="dashed", label="Alternative Path")

    # Add edge weights as labels
    edge_labels = {(u, v): f"{d:.2f}" for u, v, d in G.edges(data="weight")}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Add legend and save the figure
    plt.legend()
    if save_path:
        plt.savefig(save_path, format="png", dpi=300)
        print(f"Path visualization saved to {save_path}")
    plt.show()


def test_path_planner():
    """
    Test function to validate PathPlanner behavior.
    """
    nodes, graph = load_graph_data()
    if not nodes or not graph:
        print("Failed to load graph data.")
        return

    planner = PathPlanner(nodes, graph)

    # Test: Define start and end cities for pathfinding
    start, end = "City1", "City3"

    # Ensure start and end are valid
    if start not in planner.nodes or end not in planner.nodes:
        print(f"Invalid cities: {start} or {end} not found in the graph.")
        return

    try:
        # Find the shortest path
        path, distance, segment_distances = planner.find_shortest_path(
            start, end)
        if not path:
            print(f"No path found between {start} and {end}.")
            return

        # Print shortest path
        print("\n====================== Shortest Path ======================")
        print(f"From: {start} -> To: {end}")
        print(f"Route: {' -> '.join(path)}")
        print(f"\nTotal Distance: {distance:.2f}\n")
        print("Segment Distances:")
        for segment in segment_distances:
            print(f"  {segment[0]} -> {segment[1]}: {segment[2]:.2f}")
        print("==========================================================")

        # Visualize shortest path
        visualize_path(nodes, graph, path, save_path="shortest_path_test.png")

        # Test: Find alternative path
        penalty_factor = 2.5
        existing_paths = [(path, distance)]
        alt_result = planner.find_alternative_path_with_penalty(
            start, end, existing_paths, penalty_factor)

        if alt_result:
            # Print alternative path
            print("\n=================== Alternative Path ====================")
            print(f"From: {start} -> To: {end}")
            print(f"Route: {' -> '.join(alt_result[0])}")
            print(f"\nTotal Distance: {alt_result[1]:.2f}\n")
            print("Segment Distances:")
            for segment in alt_result[2]:
                print(f"  {segment[0]} -> {segment[1]}: {segment[2]:.2f}")
            print("==========================================================")

            # Visualize alternative path
            visualize_path(nodes, graph, path, alt_path=alt_result[0],
                           save_path="alternative_path_test.png")
        else:
            print("\nNo alternative path available.")

    except ValueError as e:
        print(f"Error during pathfinding: {e}")


if __name__ == "__main__":
    test_path_planner()
