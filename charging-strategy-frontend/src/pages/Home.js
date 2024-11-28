import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const [startCity, setStartCity] = useState("");
  const [endCity, setEndCity] = useState("");
  const [carType, setCarType] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/api/optimize", {
        startCity,
        endCity,
        carType,
      });
      navigate("/results", { state: { results: response.data } });
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Start City:
        <input
          type="text"
          value={startCity}
          onChange={(e) => setStartCity(e.target.value)}
          required
        />
      </label>
      <label>
        End City:
        <input
          type="text"
          value={endCity}
          onChange={(e) => setEndCity(e.target.value)}
          required
        />
      </label>
      <label>
        Car Type:
        <select value={carType} onChange={(e) => setCarType(e.target.value)} required>
          <option value="">Select a car</option>
          <option value="Model3LR">Model 3 Long Range</option>
          <option value="Semi">Semi Truck</option>
        </select>
      </label>
      <button type="submit">Submit</button>
    </form>
  );
};

export default Home;
