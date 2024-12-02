const form = document.getElementById("planner-form");
const results = document.getElementById("results");
const errorElement = document.getElementById("error");

form.addEventListener("submit", async (event) => {
  event.preventDefault(); // Prevent form from refreshing the page

  // Get form data
  const startCity = document.getElementById("start-city").value;
  const endCity = document.getElementById("end-city").value;
  const carType = document.getElementById("car-type").value;

  // Clear previous results or errors
  results.innerHTML = "";
  errorElement.textContent = "";

  try {
    // Make API request
    const response = await fetch("http://127.0.0.1:5000/api/optimal-route", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ start_city: startCity, end_city: endCity, car_type: carType }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    displayResults(data); // Display the data nicely
  } catch (error) {
    console.error("Error:", error);
    errorElement.textContent = `Error: ${error.message}`;
  }
});

function displayResults(data) {
  if (data.error) {
    results.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
    return;
  }

  // Render results in a clean format
  results.innerHTML = `
    <h3>Shortest Path</h3>
    <p>${data.shortest_path.join(" → ")}</p>
    <h3>Total Distance</h3>
    <p>${data.total_distance} km</p>
    <h3>Optimal Charging Strategy</h3>
    <ul>
      ${data.optimal_strategy.map(
        (step) =>
          `<li>${step.station}: Charge ${step.charge_amount}% (Departure SoC: ${step.departure_soc}%)</li>`
      ).join("")}
    </ul>
    <h3>Travel Times</h3>
    <p>Total Time: ${data.total_time.toFixed(2)} hours</p>
    <p>Charging Time: ${data.charging_time.toFixed(2)} hours</p>
    <p>Driving Time: ${data.driving_time.toFixed(2)} hours</p>
  `;
}
