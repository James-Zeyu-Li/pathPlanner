import React, { useEffect, useState } from "react";
import axios from "axios";

const MapVisualization = () => {
  const [map, setMap] = useState(null);

  useEffect(() => {
    const fetchMap = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/map", {
          responseType: "arraybuffer",
        });
        const base64 = btoa(
          new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), "")
        );
        setMap(`data:image/png;base64,${base64}`);
      } catch (error) {
        console.error("Error loading map:", error);
      }
    };
    fetchMap();
  }, []);

  if (!map) {
    return <p>Loading map...</p>;
  }

  return <img src={map} alt="Graph Visualization" style={{ width: "100%" }} />;
};

export default MapVisualization;
