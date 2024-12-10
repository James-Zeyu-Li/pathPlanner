import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Ensure the backend is running on this URL
});

// Fetch the shortest path between two cities
export const getShortestPath = async (startCity, endCity) => {
  try {
    const response = await api.post('/shortest-path', { start_city: startCity, end_city: endCity });
    return response.data;
  } catch (error) {
    console.error("API Error (Shortest Path):", error.response || error.message);
    throw error.response?.data || error.message;
  }
};

// Optimize the charging strategy
export const optimizeCharging = async (carType, segmentDistances) => {
  try {
    const response = await api.post('/optimize-charging', { car_type: carType, segment_distances: segmentDistances });
    return response.data;
  } catch (error) {
    console.error("API Error (Optimize Charging):", error.response || error.message);
    throw error.response?.data || error.message;
  }
};

// Use the traditional charging strategy
export const getTraditionalCharging = async (carType, segmentDistances) => {
  try {
    const response = await api.post('/traditional-charging', { car_type: carType, segment_distances: segmentDistances });
    return response.data;
  } catch (error) {
    console.error("API Error (Traditional Charging):", error.response || error.message);
    throw error.response?.data || error.message;
  }
};
