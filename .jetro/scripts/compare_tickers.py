import json
import urllib.request
import os

def analyze_ticker(ticker):
    url = 'http://localhost:8000/analyze'
    payload = json.dumps({"ticker": ticker, "question": "Provide a brief analysis."}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return {
                "ticker": ticker,
                "score": result.get("overall_sentiment", 0),
                "verdict": result.get("verdict", "UNKNOWN"),
                "best_analyst": "Quant" if result.get("overall_sentiment", 0) > 60 else "Macro" # simplified
            }
    except Exception as e:
        return {
            "ticker": ticker,
            "score": 0,
            "verdict": "ERROR",
            "best_analyst": "N/A"
        }

def main():
    watchlist = ["RELIANCE.NS", "INFY.NS", "HDFCBANK.NS"]
    results = []
    
    for ticker in watchlist:
        res = analyze_ticker(ticker)
        results.append(res)
        
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Generate Markdown Table
    markdown = "## WATCHLIST RANKING\n\n"
    markdown += "| Ticker | Score | Verdict | Consensus Driver |\n"
    markdown += "|---|---|---|---|\n"
    
    for r in results:
        markdown += f"| **{r['ticker']}** | {r['score']} | {r['verdict']} | {r['best_analyst']} |\n"
        
    print(markdown)

if __name__ == "__main__":
    main()
