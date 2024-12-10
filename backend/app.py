from flask import Flask, jsonify, request
from path_planner_package.path_planner import PathPlanner
from charging_strategy_optimizer.charging_strategy_optimizer import (
    load_car,
    load_path_planner,
    optimize_charging_strategy,
    traditional_strategy
)
from pathlib import Path
import json
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

# Add your existing routes here...
@app.route('/')
def index():
    return jsonify({"message": "PathPlanner API is running"})


# Paths to data files
DATA_DIR = Path(__file__).resolve().parent / "data"
NODES_FILE = DATA_DIR / "nodes.json"
GRAPH_FILE = DATA_DIR / "graph.json"
CARS_FILE = DATA_DIR / "Cars.json"

# Load data and initialize PathPlanner
try:
    with open(NODES_FILE, 'r') as f:
        nodes = json.load(f)

    with open(GRAPH_FILE, 'r') as f:
        graph = json.load(f)

    planner = PathPlanner(nodes=nodes, graph=graph)
except FileNotFoundError as e:
    print(f"Error: {e}")
    planner = None  # If initialization fails, the planner will be unavailable
except json.JSONDecodeError as e:
    print(f"Error in JSON format: {e}")
    planner = None
@app.route('/shortest-path', methods=['POST'])
def get_shortest_path():
    try:
        data = request.json
        start_city = data.get('start_city')
        end_city = data.get('end_city')

        if not start_city or not end_city:
            return jsonify({"error": "Start city and end city are required"}), 400

        # Log input data
        app.logger.info(f"Received request: start_city={start_city}, end_city={end_city}")

        # Call PathPlanner
        shortest_path, total_distance, segment_distances = planner.find_shortest_path(start_city, end_city)

        # Log the result
        app.logger.info(f"Shortest path: {shortest_path}, Total distance: {total_distance}")

        return jsonify({
            "shortest_path": shortest_path,
            "total_distance": total_distance,
            "segment_distances": segment_distances
        })
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route('/optimize-charging', methods=['POST'])
def optimize_charging():
    """Endpoint to optimize the charging strategy."""
    try:
        data = request.json
        car_type = data.get('car_type', 'Semi')

        # Load vehicle parameters
        vehicle_params = load_car(CARS_FILE, car_type)

        # Get segment distances from input
        segment_distances = data.get('segment_distances')
        if not segment_distances:
            return jsonify({"error": "Segment distances are required"}), 400

        # Convert segment distances to charging stations
        charging_stations = load_path_planner(segment_distances)

        # Optimize charging strategy
        optimal_strategy, total_time_optimal, total_charging_time_optimal, total_driving_time_optimal = optimize_charging_strategy(
            charging_stations, vehicle_params, vehicle_params['charging_curve']
        )

        return jsonify({
            "optimal_strategy": optimal_strategy,
            "total_time_optimal": total_time_optimal,
            "total_charging_time_optimal": total_charging_time_optimal,
            "total_driving_time_optimal": total_driving_time_optimal
        })
    except FileNotFoundError as e:
        return jsonify({"error": f"File not found: {e}"}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Server Error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

@app.route('/traditional-charging', methods=['POST'])
def traditional_charging():
    """Endpoint to calculate the traditional charging strategy."""
    try:
        data = request.json
        car_type = data.get('car_type', 'Semi')

        # Load vehicle parameters
        vehicle_params = load_car(CARS_FILE, car_type)

        # Get segment distances from input
        segment_distances = data.get('segment_distances')
        if not segment_distances:
            return jsonify({"error": "Segment distances are required"}), 400

        # Convert segment distances to charging stations
        charging_stations = load_path_planner(segment_distances)

        # Calculate traditional charging strategy
        traditional_strategy_result, total_time_traditional, total_charging_time_traditional, total_driving_time_traditional = traditional_strategy(
            charging_stations, vehicle_params, vehicle_params['charging_curve']
        )

        return jsonify({
            "traditional_strategy": traditional_strategy_result,
            "total_time_traditional": total_time_traditional,
            "total_charging_time_traditional": total_charging_time_traditional,
            "total_driving_time_traditional": total_driving_time_traditional
        })
    except FileNotFoundError as e:
        return jsonify({"error": f"File not found: {e}"}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    """Default endpoint for health check."""
    return jsonify({"message": "PathPlanner API is running"})


if __name__ == '__main__':
    app.run(debug=True)
