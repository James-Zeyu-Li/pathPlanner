"""
Path planner implementation using Dijkstra's algorithm for finding
shortest paths between cities.
Loads city and road network data from JSON files and provides
path finding capabilities.
"""

import json
import heapq
from pathlib import Path


class PathPlanner:
    def __init__(self, nodes=None, graph=None):
        """
        Initialize with optional nodes and graph data, or load from files
        """
        try:
            self.nodes = nodes if nodes else self._load_nodes()
            self.graph = graph if graph else self._load_graph()
            self._validate_graph()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Failed to load data: {e}")

    def _validate_graph(self):
        """Validate graph structure and consistency"""
        if not isinstance(self.graph, dict):
            raise ValueError("Graph must be a dictionary")

        # Validate edges and weights
        for node, edges in self.graph.items():
            if not isinstance(edges, dict):
                raise ValueError(f"Edges for node {node} must be a dictionary")
            for target, weight in edges.items():
                if weight < 0:
                    raise ValueError(
                        f"Negative weight found between {node} and {target}")
                # Validate undirected graph consistency
                if node not in self.graph.get(target, {}):
                    raise ValueError(
                        f"Missing reciprocal edge between {target} and {node}")
                if weight != self.graph[target][node]:
                    raise ValueError(
                        f"Inconsistent weights between {node} and {target}")

    @staticmethod
    def _load_nodes():
        """
        Load nodes data from JSON file
        """
        try:
            with open(Path('data/nodes.json')) as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in nodes.json")

    @staticmethod
    def _load_graph():
        """
        Load graph data from JSON file
        """
        try:
            with open(Path('data/graph.json')) as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in graph.json")

    def connected_by_road(self, node):
        """
        Find all cities connected by road to the input city
        """
        return list(self.graph.get(node, {}).keys())

    def find_shortest_path(self, start, end, graph=None):
        """
        Find shortest path between start and end using Dijkstra's algorithm
        """
        if graph is None:
            graph = self.graph

        if start not in graph:
            raise ValueError(f"Start city {start} not found in graph")

        if end not in graph:
            raise ValueError(f"End city {end} not found in graph")

        queue = [(0, start)]  # (distance, node) start from 0 distance
        # All distances are infinity at the beginning
        distances = {node: float('inf') for node in graph}
        # When start, all previous nodes are None
        previous_nodes = {node: None for node in graph}
        distances[start] = 0
        visited = set()

        while queue:  # while queue is not empty
            # get the node with the smallest distance
            current_distance, current_node = heapq.heappop(queue)

            # if the node has been visited, skip
            if current_node in visited:
                continue

            visited.add(current_node)  # mark the current node as visited

            for neighbor in self.connected_by_road(current_node):
                distance = current_distance + graph[current_node][neighbor]

                # if a shorter path is found, update the distance
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
                    previous_nodes[neighbor] = current_node

            if current_node == end:  # if we reach the end node, path found
                path = self._reconstruct_path(previous_nodes, start, end)
                segment_distances = [
                    (path[i], path[i + 1], graph[path[i]][path[i + 1]])
                    for i in range(len(path) - 1)
                ]
                total_distance = distances[end]
                return path, total_distance, segment_distances

        return None, float('inf')  # No path found

    def _reconstruct_path(self, previous, start, end):
        """
        Reconstruct path from start to end using previous nodes
        """
        path = []
        current = end
        visited = set()

        while current is not None:
            if current in visited:
                raise ValueError("Circular path detected")
            visited.add(current)
            path.append(current)
            current = previous[current]

        path.reverse()
        if not path or path[0] != start:
            raise ValueError("Path reconstruction failed!")
        return path

    def get_path_distance(self, path):
        """
        Get the total distance of the input path
        """
        if not path or len(path) < 2:
            return 0
        return sum(
            self.graph[path[i]][path[i + 1]]
            for i in range(len(path) - 1)
        )

    def create_penalized_graph(self, existing_paths, penalty_factor):
        """
        Create new graph with penalized weights for existing paths
        """
        if not isinstance(penalty_factor, (int, float)) or penalty_factor <= 0:
            raise ValueError("Penalty factor must be a positive number")

        modified_graph = {
            node: neighbors.copy()
            for node, neighbors in self.graph.items()
        }

        for path in existing_paths:
            if isinstance(path, tuple):
                path = path[0]  # Extract path from (path, distance) tuple
            for i in range(len(path) - 1):
                node1, node2 = path[i], path[i + 1]
                if node2 in modified_graph[node1]:
                    modified_graph[node1][node2] *= penalty_factor
                if node1 in modified_graph[node2]:
                    modified_graph[node2][node1] *= penalty_factor

        return modified_graph

    def find_alternative_path_with_penalty(self, start, end,
                                           existing_paths, penalty_factor):
        """
        Find shortest path between start and end with penalties
        for existing paths
        """
        if not isinstance(penalty_factor, (int, float)) or penalty_factor < 2 or penalty_factor > 10:
            raise ValueError("Penalty factor must be between 2 and 10")

        modified_graph = self.create_penalized_graph(
            existing_paths, penalty_factor)

        # Find shortest path in penalized graph
        new_path, penalized_distance, segment_distances = \
            self.find_shortest_path(
                start, end, graph=modified_graph)

        # Check path validity
        if not new_path or any(new_path == path[0] for path in existing_paths):
            return None

        # Calculate actual distance using original graph
        distance_without_penalty = self.get_path_distance(new_path)

        segment_distances = [
            (new_path[i], new_path[i + 1],
             self.graph[new_path[i]][new_path[i + 1]])
            for i in range(len(new_path) - 1)
        ]

        return new_path, distance_without_penalty, segment_distances
