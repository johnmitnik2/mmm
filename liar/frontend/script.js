async function run() {
  const input = document.getElementById("input").value;
  const output = document.getElementById("output");

  output.textContent = "Thinking badly...";

  const res = await fetch("https://YOUR-BACKEND-URL/advice", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input })
  });

  const data = await res.json();
  output.textContent = data.response;
}