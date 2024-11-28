import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import ResultsPage from "./pages/ResultsPage";

const App = () => {
  return (
    <Router>
      <div>
        <h1>Charging Strategy Optimization</h1>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
