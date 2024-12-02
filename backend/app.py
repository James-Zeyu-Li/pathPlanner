from flask import Flask, request, jsonify
from flask_cors import CORS
from path_planner_package.path_planner import PathPlanner
from charging_strategy_optimizer.charging_strategy_optimizer import (
    load_car,
    optimize_charging_strategy,
    load_path_planner,
)

app = Flask(__name__)
CORS(app)  # Enable CORS to allow communication with the frontend

# Load required files
CAR_FILE = "data/Cars.json"
NODES_FILE = "data/nodes.json"
GRAPH_FILE = "data/graph.json"

# Initialize Path Planner
planner = PathPlanner()

@app.route("/")
def home():
    return "Welcome to the Path Planner API"
@app.route('/api/optimal-route', methods=['POST'])
def optimal_route():
    try:
        data = request.get_json()
        if not all(k in data for k in ('start_city', 'end_city', 'car_type')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        start_city = data['start_city']
        end_city = data['end_city']
        car_type = data['car_type']

        # Call the path-planning function
        path, total_distance, segment_distances = planner.find_shortest_path(start_city, end_city)
        if not path:
            return jsonify({'error': 'Path not found'}), 400

        car_data = load_car('data/Cars.json', car_type)
        charging_stations = load_path_planner(segment_distances)
        strategy, total_time, charging_time, driving_time = optimize_charging_strategy(
            charging_stations, car_data, car_data['charging_curve']
        )

        return jsonify({
            'path': path,
            'total_distance': total_distance,
            'segment_distances': segment_distances,
            'strategy': strategy,
            'total_time': total_time,
            'charging_time': charging_time,
            'driving_time': driving_time
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
