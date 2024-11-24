import unittest
from path_planner import PathPlanner


class TestPathPlannerWithMapData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.planner = PathPlanner(
            nodes={
                "City1": {"type": "city", "location": [0, 0]},
                "City2": {"type": "city", "location": [50, 50]},
                "City3": {"type": "city", "location": [100, 100]},
                "City5": {"type": "city", "location": [150, 150]},
            },
            graph={
                "City1": {"City2": 70, "City3": 120},
                "City2": {"City1": 70, "City5": 80},
                "City3": {"City1": 120, "City5": 60},
                "City5": {"City2": 80, "City3": 60},
            },
        )

    def test_shortest_paths(self):
        """Test shortest paths with known results"""
        test_cases = [
            # (start, end, expected_path, expected_distance)
            ("City1", "City2", ["City1", "City2"], 70),           # Direct path
            # Through City2
            ("City1", "City5", ["City1", "City2", "City5"], 150),
            ("City1", "City3", ["City1", "City3"], 120),          # Direct path
            # Through City5
            ("City2", "City3", ["City2", "City5", "City3"], 140),
            ("City3", "City5", ["City3", "City5"], 60),           # Direct path
            ("City2", "City5", ["City2", "City5"], 80),           # Direct path
        ]

        for start, end, expected_path, expected_distance in test_cases:
            with self.subTest(f"Testing path from {start} to {end}"):
                path, distance = self.planner.find_shortest_path(start, end)

                # Verify path matches expected
                self.assertEqual(
                    path,
                    expected_path,
                    f"Path mismatch from {start} to {end}:\n"
                    f"Expected: {' -> '.join(expected_path)}\n"
                    f"Got: {' -> '.join(path)}"
                )

                # Verify distance matches expected
                self.assertEqual(
                    distance,
                    expected_distance,
                    f"Distance mismatch from {start} to {end}:\n"
                    f"Expected: {expected_distance}\n"
                    f"Got: {distance}"
                )

                # Verify each step in path exists in graph
                for i in range(len(path) - 1):
                    node1, node2 = path[i], path[i + 1]
                    self.assertIn(
                        node2,
                        self.planner.graph[node1],
                        f"Invalid edge: {node1} -> {node2}"
                    )

                # Verify calculated distance matches returned distance
                calculated_distance = sum(
                    self.planner.graph[path[i]][path[i + 1]]
                    for i in range(len(path) - 1)
                )
                self.assertEqual(
                    calculated_distance,
                    distance,
                    f"Calculated distance {calculated_distance} "
                    f"doesn't match returned distance {distance}"
                )


if __name__ == '__main__':
    unittest.main()
