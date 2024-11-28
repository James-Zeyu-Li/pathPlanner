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


# 创建指定拓扑结构的图
def create_custom_structure():
    nodes = {
        "City1": {"type": "city", "location": (0, 200)},
        "City2": {"type": "city", "location": (350, 1000)},
        "City3": {"type": "city", "location": (950, 900)},
        "City4": {"type": "city", "location": (1000, 150)},
        "City5": {"type": "city", "location": (550, 0)},
    }
    graph = {}

    # 添加城市之间的连接
    connections = {
        "City1": ["City2", "City4", "City5"],
        "City2": ["City1", "City3", "City4", "City5"],
        "City3": ["City2", "City4", "City5"],
        "City4": ["City1", "City2", "City3", "City5"],
        "City5": ["City1", "City2", "City3", "City4"],
    }

    # 为每对城市之间生成充电站
    processed_paths = set()  # 存储已处理路径
    station_id = 1  # 初始化充电站 ID

    for city, neighbors in connections.items():
        for neighbor in neighbors:
            # 检查是否已经处理过该路径
            if (city, neighbor) in processed_paths or \
               (neighbor, city) in processed_paths:
                continue

            # 标记路径为已处理
            processed_paths.add((city, neighbor))

            # 计算城市之间的距离
            city_loc = nodes[city]["location"]
            neighbor_loc = nodes[neighbor]["location"]

            # 确保充电站位于主路上
            num_stations = random.randint(1, 8)
            station_nodes = []
            for _ in range(num_stations):
                t = random.uniform(0.1, 1)  # 插值比例
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

            # 连接充电站到路径上的城市和其他充电桩
            prev_node = city
            for station in station_nodes:
                dist = calculate_distance(
                    nodes[prev_node]["location"], nodes[station]["location"])
                graph.setdefault(prev_node, {})[station] = dist
                graph.setdefault(station, {})[prev_node] = dist
                prev_node = station

            # 最后一个充电桩连接到目标城市
            final_dist = calculate_distance(
                nodes[prev_node]["location"], neighbor_loc)
            graph.setdefault(prev_node, {})[neighbor] = final_dist
            graph.setdefault(neighbor, {})[prev_node] = final_dist

    return nodes, graph

# 可视化图


def visualize_custom_graph(graph, nodes, save_path=None):
    G = nx.Graph()

    # 添加节点和边
    for node, edges in graph.items():
        for neighbor, distance in edges.items():
            G.add_edge(node, neighbor, weight=distance)

    # 设置节点颜色
    colors = []
    labels = {}
    for node in G.nodes:
        if nodes[node]["type"] == "city":
            colors.append("red")  # 城市为红色
            labels[node] = node
        else:
            colors.append("blue")  # 充电站为蓝色
            labels[node] = node  # 标记充电站编号

    # 使用实际坐标进行布局
    pos = {node: nodes[node]["location"] for node in G.nodes}
# 获取无向图中的边权重
    edge_labels = {(u, v): d for u, v, d in G.edges(data="weight") if u < v}

    # 绘制图
    nx.draw(G, pos, with_labels=True, labels=labels,
            node_size=700, node_color=colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # 保存图像
    if save_path:
        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, format="png", dpi=300)

    # 显示图像
    plt.show()


# 保存数据到 JSON 文件
def save_to_file(data, filepath):
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"保存数据到文件失败: {e}")


# 从 JSON 文件加载数据
def load_from_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"加载数据失败: {e}")
        return None


if __name__ == "__main__":
    # 创建自定义拓扑结构
    nodes, graph = create_custom_structure()

    # 定义文件路径
    nodes_file = "data/nodes.json"
    graph_file = "data/graph.json"
    image_file = "data/graph_visualization.png"  # 图片保存路径

    # 保存到 JSON 文件
    save_to_file(nodes, nodes_file)
    save_to_file(graph, graph_file)

    # 可视化并保存图像
    visualize_custom_graph(graph, nodes, save_path=image_file)

    # 验证数据保存后是否能正确加载
    loaded_nodes = load_from_file(nodes_file)
    loaded_graph = load_from_file(graph_file)
