import json
# pyrefly: ignore [missing-import]
from jet.market import Ticker

def main():
    try:
        t = Ticker("RELIANCE.NS")
        info = t.fast_info
        
        # fast_info doesn't include P/E, but let's grab what we can to make it fast
        data = {
            "price": round(info.last_price, 2),
            "dayHigh": round(info.day_high, 2),
            "dayLow": round(info.day_low, 2),
            "volume": int(info.last_volume),
            "fiftyTwoWeekHigh": round(info.year_high, 2),
            "fiftyTwoWeekLow": round(info.year_low, 2),
            "ticker": "RELIANCE.NS"
        }
        
        print(json.dumps(data))
    except Exception as e:
        # Fallback empty data so it doesn't crash the JSON parser
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
