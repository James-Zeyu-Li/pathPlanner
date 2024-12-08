import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math


def load_nodes(file_path):
    """
    load nodes from json file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise FileNotFoundError(f"Can't find path: {file_path}: {e}")


def calculate_distance(coord1, coord2):
    """
    calculate distance between two coordinates
    """
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)


def generate_adjacency_list_with_distance(paths, nodes, base_distance=55, base_pair=("Vancouver", "Abbotsford")):
    """
    according to the paths and nodes, generate adjacency list with distance
    """
    # 计算比例因子
    if base_pair[0] in nodes and base_pair[1] in nodes:
        base_coord1 = nodes[base_pair[0]]["location"]
        base_coord2 = nodes[base_pair[1]]["location"]
        base_actual_distance = calculate_distance(base_coord1, base_coord2)
        scale_factor = base_distance / base_actual_distance
    else:
        raise ValueError(f" {base_pair} Does not exist in the nodes data")

    adjacency_list = {}
    for path in paths:
        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]

            # make sure the city1 and city2 are in the nodes
            if city1 in nodes and city2 in nodes:
                if city1 not in adjacency_list:
                    adjacency_list[city1] = {}
                if city2 not in adjacency_list:
                    adjacency_list[city2] = {}

                # get the distance between city1 and city2
                coord1 = nodes[city1]["location"]
                coord2 = nodes[city2]["location"]
                distance = calculate_distance(coord1, coord2) * scale_factor
                distance = round(distance, 2)

                # update the adjacency list
                adjacency_list[city1][city2] = distance
                adjacency_list[city2][city1] = distance
    return adjacency_list


def save_adjacency_list(adjacency_list, file_path):
    """
    save the adjacency list to a json file
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(adjacency_list, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Fail to save: {e}")


def visualize_paths(nodes, paths, adjacency_list, save_path=None):
    """
    Visualize the paths on the map
    """
    G = nx.Graph()
    pos = {}

    for node, data in nodes.items():
        if "location" not in data:
            continue
        lat, lon = data["location"]
        x, y = lon, lat  # use the longitude as x and latitude as y
        pos[node] = (x, y)
        G.add_node(node, type=data["type"])

    # add edges
    for city1, neighbors in adjacency_list.items():
        for city2, weight in neighbors.items():
            G.add_edge(city1, city2, weight=weight)

    plt.figure(figsize=(15, 10))

    node_colors = [
        "red" if nodes[node]["type"].lower() == "city" else "blue" for node, data in nodes.items()
    ]
    node_sizes = [
        1000 if nodes[node]["type"].lower() == "city" else 500 for node, data in nodes.items()
    ]

    nx.draw_networkx_edges(G, pos, edge_color='grey', alpha=0.5)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                           node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={
                                 k: f"{v} km" for k, v in edge_labels.items()}, font_size=8)

    for path in paths:
        path_pos = [pos[node] for node in path if node in pos]
        plt.plot(*zip(*path_pos), marker='o', markersize=8,
                 label=" -> ".join(path), alpha=0.7)
    legend_elements = [
        Rectangle((0, 0), 1, 1, facecolor="red",
                  edgecolor="black", label="City"),
        Rectangle((0, 0), 1, 1, facecolor="blue",
                  edgecolor="black", label="Station"),
    ]
    plt.legend(handles=legend_elements, loc="upper right")

    plt.title("Pathways Visualization with Distances", fontsize=15)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, format="png", dpi=300, bbox_inches="tight")
        print(f"Picture saves to {save_path}")
    plt.show()


if __name__ == "__main__":
    nodes_file = "pathPlanner/backend/data/nodes.json"
    adjacency_list_file = "pathPlanner/backend/data/graph.json"
    image_file = "pathPlanner/backend/data/graph_visualization_routes_with_distances.png"

    nodes = load_nodes(nodes_file)

    route1 = [
        "Vancouver", "Abbotsford", "Chilliwack", "Hope", "Fraser Valley B", "Fraser Valley C", "Lake Louise",
        "Banff", "Canmore", "Kananaskis", "Calgary", "Crossfield", "Olds",
        "Bowden", "Innisfail", "Red Deer County", "Red Deer", "Edmonton International Airport",
        "Leduc", "Edmonton"
    ]
    route2 = [
        "Vancouver", "Fraser Valley A", "Lytton", "Merritt", "Barriere", "Little Fort",
        "Clearwater", "Thompson-Nicola B", "Blue River", "Valemount", "Jasper",
        "Edson Station", "Edson", "Edmonton"
    ]
    route3 = [
        "Vancouver", "Cache Creek", "Clinton", "100 Mile House", "Williams Lake", "Cariboo A",
        "Hixon", "PRINCE GEORGE", "Prince George"
    ]
    route4 = [
        "Prince George", "Dome Creek", "McBride", "Tete Jaune Cache", "Edson Station", "Edmonton"
    ]
    additional_paths = [
        ["Clearwater", "Thompson-Nicola B", "Improvement District No.9",
            "Rocky Mountain House", "Condor", "Leduc"],
        ["Thompson-Nicola B", "Lake Louise"]
    ]

    all_routes = [route1, route2, route3, route4] + additional_paths
    adjacency_list = generate_adjacency_list_with_distance(all_routes, nodes)

    save_adjacency_list(adjacency_list, adjacency_list_file)

    visualize_paths(nodes, all_routes, adjacency_list, save_path=image_file)
