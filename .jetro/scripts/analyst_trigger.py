import json
import urllib.request
import os

def main():
    try:
        # 1. Read context
        context_path = os.path.join(os.environ.get('JET_WORKSPACE', '.'), '.jetro', 'context.json')
        if os.path.exists(context_path):
            with open(context_path, 'r') as f:
                context = json.load(f)
                ticker = context.get('ticker', 'RELIANCE.NS')
        else:
            ticker = "RELIANCE.NS"

        # 2. Call FastAPI backend
        url = 'http://localhost:8000/analyze'
        payload = json.dumps({"ticker": ticker, "question": "Provide a comprehensive analysis."}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                verdict = result.get('verdict', 'UNKNOWN')
                score = result.get('overall_sentiment', 0)
        except Exception as api_e:
            # Maybe backend is down
            verdict = "ERROR"
            score = 0
            
        # 3. Format Markdown Note
        markdown = f"""## AI Analysis: {ticker}

**Verdict:** {verdict}
**Overall Signal:** {score} / 100

---
*Human Analyst Notes:*
- 
"""
        # Output JSON so Jetro merges it into the note's data.markdown
        print(json.dumps({"markdown": markdown}))
        
    except Exception as e:
        print(json.dumps({"markdown": f"## Error\n\n{str(e)}"}))

if __name__ == "__main__":
    main()
