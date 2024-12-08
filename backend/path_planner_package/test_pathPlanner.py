import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from path_planner import PathPlanner


# Relative path to data files
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

    # Define node colors
    colors = []
    for node in G.nodes:
        if node in highlighted_nodes:
            if node == path[0]:  # Start node
                colors.append('green')
            elif node == path[-1]:  # End node
                colors.append('red')
            else:  # Nodes in the path
                colors.append('orange')
        else:
            colors.append('lightgrey')

    # Draw the graph with all edges in light grey for context
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color=colors,
            node_size=700, edge_color="lightgrey", font_size=10)

    # Highlight shortest path edges
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                               edge_color="blue", width=2, label="Shortest Path")

    # Highlight alternative path edges
    if alt_edges:
        nx.draw_networkx_edges(G, pos, edgelist=alt_edges, edge_color="orange",
                               width=2, style="dashed", label="Alternative Path")

    # Add edge weights as labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={
                                 k: f"{v} km" for k, v in edge_labels.items()}, font_size=8)

    # Highlight start and end nodes
    plt.scatter(*pos[path[0]], color='green', s=1000, label="Start Node")
    plt.scatter(*pos[path[-1]], color='red', s=1000, label="End Node")

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

    # test 1 shortest path
    start, end = "Vancouver", "Edmonton"

    try:
        # find the shortest path
        path, distance, segment_distances = planner.find_shortest_path(
            start, end)
        if not path:
            print(f"No path found between {start} and {end}.")
            return

        print("\n====================== Shortest Path ======================")
        print(f"From: {start} -> To: {end}")
        print(f"Route: {' -> '.join(path)}")
        print(f"\nTotal Distance: {distance:.2f}\n")
        print("Segment Distances:")
        for segment in segment_distances:
            print(f"  {segment[0]} -> {segment[1]}: {segment[2]:.2f}")
        print("==========================================================")

        # shortest path visualization
        visualize_path(nodes, graph, path, save_path="shortest_path_test.png")

    except ValueError as e:
        print(f"Error during shortest pathfinding: {e}")

    # test 2 alternative path
    try:
        penalty_factor = 2.5
        existing_paths = [(path, distance)]
        alt_result = planner.find_alternative_path_with_penalty(
            start, end, existing_paths, penalty_factor)

        if alt_result:
            alt_path, alt_distance, alt_segments = alt_result
            print("\n=================== Alternative Path ====================")
            print(f"From: {start} -> To: {end}")
            print(f"Route: {' -> '.join(alt_path)}")
            print(f"\nTotal Distance: {alt_distance:.2f}\n")
            print("Segment Distances:")
            for segment in alt_segments:
                print(f"  {segment[0]} -> {segment[1]}: {segment[2]:.2f}")
            print("==========================================================")

            # Visualize the alternative path
            visualize_path(
                nodes, graph, path, alt_path=alt_path, save_path="alternative_path_test.png"
            )
        else:
            print("\nNo alternative path available.")
    except ValueError as e:
        print(f"Error during alternative pathfinding: {e}")

    # test 3 same start and end
    try:
        start = "Vancouver"
        path, distance, _ = planner.find_shortest_path(start, start)
        if path:
            print("\n================ Same Start and End Test ================")
            print(f"Path from {start} to {start}: {' -> '.join(path)}")
            print(f"Distance: {distance:.2f}")
            print("==========================================================")
        else:
            print("\nNo path found for same start and end test.")
    except ValueError as e:
        print(f"Error during same start and end test: {e}")

    # test 4 path not found
    try:
        start, end = "Vancouver", "NonExistentCity"
        path, distance, _ = planner.find_shortest_path(start, end)
        if not path:
            print("\n=============== Path Not Found Test ====================")
            print(f"No path found between {start} and {end}.")
            print("==========================================================")
    except ValueError as e:
        print(f"Error during path not found test: {e}")


if __name__ == "__main__":
    test_path_planner()
