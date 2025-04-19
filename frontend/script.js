document.getElementById("orderForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const order = {};
  for (const [key, value] of formData.entries()) {
    const num = parseInt(value);
    if (num > 0) order[key] = num;
  }

  // Change the URL to your Render backend
  const res = await fetch("https://railway-cost-backend.onrender.com/calculate-delivery-cost", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(order)
  });

  const data = await res.json();
  document.getElementById("result").textContent = "Minimum Delivery Cost: ₹" + data.min_cost;
});
