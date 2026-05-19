const BASE_URL = "http://localhost:8000";

export async function analyzeStock(ticker, question = "Should I invest in this stock?") {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ticker, question }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Analysis failed (${response.status}): ${text}`);
  }

  return response.json();
}

export async function analyzeStockMock() {
  const response = await fetch(`${BASE_URL}/analyze/mock`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Mock analysis failed (${response.status}): ${text}`);
  }

  return response.json();
}
