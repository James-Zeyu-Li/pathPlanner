from flask import Flask, request, jsonify

app = Flask(__name__)

# Root route
@app.route('/')
def home():
    return "Welcome to the Flask server!"

# Health check route
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "success", "message": "Flask server is running!"})

# Optimal route calculation
@app.route('/api/optimal-route', methods=['POST'])
def calculate_optimal_route():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    start_city = data.get("start_city")
    end_city = data.get("end_city")
    car_type = data.get("car_type")

    if not all([start_city, end_city, car_type]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Mock response (replace this with your actual logic)
    return jsonify({
        "start_city": start_city,
        "end_city": end_city,
        "car_type": car_type,
        "strategy": [
            {"station": "Station1", "charge_amount": 20, "departure_soc": 70},
            {"station": "Station2", "charge_amount": 30, "departure_soc": 100},
        ],
        "total_time": 5.2
    }), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
