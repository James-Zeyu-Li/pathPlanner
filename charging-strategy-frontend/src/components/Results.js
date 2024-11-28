import React from "react";

const Results = ({ data }) => {
  const { optimal, traditional } = data;

  return (
    <div>
      <h2>Optimal Strategy</h2>
      <ul>
        {optimal.map((step, index) => (
          <li key={index}>
            At {step.station}, charged from {step.departure_soc - step.charge_amount}% to {step.departure_soc}%, charged {step.charge_amount}%.
          </li>
        ))}
      </ul>
      <h2>Traditional Strategy</h2>
      <ul>
        {traditional.map((step, index) => (
          <li key={index}>
            At {step.station}, charged from {step.departure_soc - step.charge_amount}% to {step.departure_soc}%, charged {step.charge_amount}%.
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Results;
