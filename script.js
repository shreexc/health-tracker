const API_BASE = "http://127.0.0.1:8000";

document
  .getElementById("diagnoseBtn")
  .addEventListener("click", async function () {
    const symptoms = document.getElementById("symptoms").value.trim();
    const resultEl = document.getElementById("result");
    if (!symptoms) return;

    resultEl.textContent = "Loading...";

    try {
      const res = await fetch(`${API_BASE}/diagnose`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms }),
      });
      const data = await res.json();
      resultEl.textContent = res.ok ? data.diagnosis : `Error: ${data.error}`;
    } catch (err) {
      resultEl.textContent = `Fetch error: ${err.message}`;
      resultEl.classList.add("error");
    }
  });

fetch(`${API_BASE}/health`)
  .then((r) => r.json())
  .then((data) => console.log("Health:", data));