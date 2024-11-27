import json
from pathlib import Path
from path_planner import PathPlanner


# 文件路径配置
DATA_DIR = Path(__file__).resolve().parent / "data"
NODES_FILE = DATA_DIR / "nodes.json"
GRAPH_FILE = DATA_DIR / "graph.json"


def load_graph_data():
    """从文件加载节点和图数据"""
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


def prompt_city_selection(planner, prompt):
    """提示用户选择一个城市"""
    cities = [node for node, details in planner.nodes.items()
              if details.get("type") == "city"]
    if not cities:
        print("No cities available in the graph.")
        return None

    print(f"\nAvailable Cities:")
    for idx, city in enumerate(cities, start=1):
        print(f"{idx}. {city}")

    while True:
        try:
            selection = int(input(prompt).strip())
            if 1 <= selection <= len(cities):
                return cities[selection - 1]
            else:
                print(f"Please select a number between 1 and {len(cities)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def prompt_penalty_factor():
    """提示用户输入一个惩罚系数"""
    while True:
        try:
            penalty_factor = float(
                input("Enter penalty factor (e.g., 2.0): ").strip())
            if penalty_factor > 0:
                return penalty_factor
            else:
                print("Penalty factor must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def display_path_info(start, end, path, distance, segment_distances):
    """格式化显示路径信息"""
    print(f"\nShortest path from {start} to {end}:")
    print(f"Route: {' -> '.join(path)}")
    print(f"Total Distance: {distance:.2f}")
    print("Segment Distances:")
    for seg in segment_distances:
        print(f"  {seg[0]} -> {seg[1]}: {seg[2]:.2f}")


def main():
    """主函数：运行路径规划程序"""
    # 加载数据并初始化规划器
    nodes, graph = load_graph_data()
    if not nodes or not graph:
        return

    planner = PathPlanner(nodes, graph)

    # 提示用户选择起点和终点城市
    start = prompt_city_selection(planner, "Select start city (number): ")
    if not start:
        return

    end = prompt_city_selection(planner, "Select destination city (number): ")
    if not end:
        return

    # 查找最短路径
    try:
        path, distance, segment_distances = planner.find_shortest_path(
            start, end)
        if not path:
            print(f"No path found between {start} and {end}.")
            return

        display_path_info(start, end, path, distance, segment_distances)

        # 提示用户输入惩罚系数并查找备用路径
        penalty_factor = prompt_penalty_factor()
        existing_paths = [(path, distance)]
        alt_result = planner.find_alternative_path_with_penalty(
            start, end, existing_paths, penalty_factor
        )
        if alt_result:
            alt_path, actual_distance, alt_segment_distances = alt_result
            print("\nAlternative Path Found:")
            display_path_info(start, end, alt_path,
                              actual_distance, alt_segment_distances)
        else:
            print("\nNo alternative path available.")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
