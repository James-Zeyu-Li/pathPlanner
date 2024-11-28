import React from "react";
import { useLocation } from "react-router-dom";
import Results from "../components/Results";
import MapVisualization from "../components/MapVisualization";

const ResultsPage = () => {
  const location = useLocation();
  const { results } = location.state;

  return (
    <div>
      <Results data={results} />
      <MapVisualization />
    </div>
  );
};

export default ResultsPage;
