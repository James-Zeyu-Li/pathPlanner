import React, { useState } from 'react';
import { getShortestPath, optimizeCharging, getTraditionalCharging } from './api';

function App() {
  const [startCity, setStartCity] = useState('');
  const [endCity, setEndCity] = useState('');
  const [carType, setCarType] = useState('Semi');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleShortestPath = async () => {
    try {
      console.log("Requesting shortest path for:", { startCity, endCity });
      const data = await getShortestPath(startCity, endCity);
      console.log("Shortest path response:", data);
      setResult(data);
      setError(null); // Clear any previous errors
    } catch (err) {
      console.error("Error fetching shortest path:", err);
      setError(err);
      alert(typeof err === 'object' ? JSON.stringify(err, null, 2) : err);
    }
  };

  const handleOptimizeCharging = async () => {
    try {
      const segmentDistances = result?.segment_distances || [];
      console.log("Optimizing charging with:", { carType, segmentDistances });
      const data = await optimizeCharging(carType, segmentDistances);
      console.log("Optimized charging response:", data);
      setResult(data);
      setError(null); // Clear any previous errors
    } catch (err) {
      console.error("Error optimizing charging:", err);
      setError(err);
      alert(typeof err === 'object' ? JSON.stringify(err, null, 2) : err);
    }
  };

  const handleTraditionalCharging = async () => {
    try {
      const segmentDistances = result?.segment_distances || [];
      console.log("Traditional charging with:", { carType, segmentDistances });
      const data = await getTraditionalCharging(carType, segmentDistances);
      console.log("Traditional charging response:", data);
      setResult(data);
      setError(null); // Clear any previous errors
    } catch (err) {
      console.error("Error with traditional charging:", err);
      setError(err);
      alert(typeof err === 'object' ? JSON.stringify(err, null, 2) : err);
    }
  };

  return (
    <div>
      <h1>Path Planner & Charging Strategy</h1>
      <div>
        <input
          type="text"
          placeholder="Start City"
          value={startCity}
          onChange={(e) => setStartCity(e.target.value)}
        />
        <input
          type="text"
          placeholder="End City"
          value={endCity}
          onChange={(e) => setEndCity(e.target.value)}
        />
        <button onClick={handleShortestPath}>Find Shortest Path</button>
      </div>

      {error && (
        <div style={{ color: 'red', marginTop: '20px' }}>
          <h3>Error:</h3>
          <pre>{JSON.stringify(error, null, 2)}</pre>
        </div>
      )}

      {result && (
        <div>
          <h2>Result</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
          <button onClick={handleOptimizeCharging}>Optimize Charging</button>
          <button onClick={handleTraditionalCharging}>Traditional Charging</button>
        </div>
      )}
    </div>
  );
}

export default App;
