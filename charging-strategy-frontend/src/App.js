import React, { useState } from "react";
import "./styles.css";

function App() {
  const [startCity, setStartCity] = useState("");
  const [endCity, setEndCity] = useState("");
  const [carType, setCarType] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      start_city: startCity,
      end_city: endCity,
      car_type: carType,
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/api/optimal-route", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      setError("");
    } catch (error) {
      console.error("Error:", error);
      setError(`Error: ${error.message}`);
      setResult(null);
    }
  };

  return (
    <div className="container">
      <h1>Path Planner</h1>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="startCity">Start City:</label>
          <input
            type="text"
            id="startCity"
            value={startCity}
            onChange={(e) => setStartCity(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="endCity">End City:</label>
          <input
            type="text"
            id="endCity"
            value={endCity}
            onChange={(e) => setEndCity(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="carType">Car Type:</label>
          <input
            type="text"
            id="carType"
            value={carType}
            onChange={(e) => setCarType(e.target.value)}
            required
          />
        </div>
        <button type="submit">Calculate Route</button>
      </form>
      <div className="results">
        <h2>Results</h2>
        {error && <p className="error">{error}</p>}
        {result && (
          <div>
            <p><strong>Path:</strong> {result.path.join(" → ")}</p>
            <p><strong>Total Distance:</strong> {result.total_distance} km</p>
            <p><strong>Total Time:</strong> {result.total_time.toFixed(2)} hours</p>
            <p><strong>Charging Time:</strong> {result.charging_time.toFixed(2)} hours</p>
            <p><strong>Driving Time:</strong> {result.driving_time.toFixed(2)} hours</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
