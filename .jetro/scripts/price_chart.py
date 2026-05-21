import json
import yfinance as yf

def get_chart_data():
    try:
        # Use yfinance directly to get history
        t = yf.Ticker("RELIANCE.NS")
        hist = t.history(period="1mo")
        
        # Prepare Plotly trace
        dates = [d.strftime("%Y-%m-%d") for d in hist.index]
        closes = [round(c, 2) for c in hist['Close']]
        
        trace = {
            "x": dates,
            "y": closes,
            "type": "scatter",
            "mode": "lines",
            "name": "RELIANCE.NS",
            "line": {"color": "#10b981", "width": 2}
        }
        
        layout = {
            "title": "Price History — RELIANCE.NS",
            "plot_bgcolor": "#171717",
            "paper_bgcolor": "#171717",
            "font": {"color": "#e5e7eb"},
            "xaxis": {"gridcolor": "#262626"},
            "yaxis": {"gridcolor": "#262626"}
        }
        
        data = {
            "title": "Price History — RELIANCE.NS",
            "traces": [trace],
            "plotlyLayout": layout
        }
        print(json.dumps(data))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    get_chart_data()
