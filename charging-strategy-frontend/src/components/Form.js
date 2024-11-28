import React, { useState } from "react";

const Form = ({ onSubmit }) => {
  // Local state for form fields
  const [startCity, setStartCity] = useState(""); // To store the start city
  const [endCity, setEndCity] = useState(""); // To store the end city
  const [carType, setCarType] = useState(""); // To store the selected car type

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent the default form submission behavior
    // Call the parent `onSubmit` function with the form data
    onSubmit({ startCity, endCity, carType });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>
          Start City:
          <input
            type="text"
            value={startCity}
            onChange={(e) => setStartCity(e.target.value)} // Update `startCity` state
            required // Make the field required
          />
        </label>
      </div>

      <div>
        <label>
          End City:
          <input
            type="text"
            value={endCity}
            onChange={(e) => setEndCity(e.target.value)} // Update `endCity` state
            required // Make the field required
          />
        </label>
      </div>

      <div>
        <label>
          Car Type:
          <select
            value={carType}
            onChange={(e) => setCarType(e.target.value)} // Update `carType` state
            required // Make the field required
          >
            <option value="">Select a car</option>
            <option value="Model3LR">Model 3 Long Range</option>
            <option value="Semi">Semi Truck</option>
          </select>
        </label>
      </div>

      <div>
        <button type="submit">Submit</button> {/* Button to submit the form */}
      </div>
    </form>
  );
};

export default Form;
