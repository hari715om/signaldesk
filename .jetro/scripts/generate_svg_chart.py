import os

dates = [
    "2026-04-06", "2026-04-07", "2026-04-08", "2026-04-09", "2026-04-10", 
    "2026-04-13", "2026-04-15", "2026-04-16", "2026-04-17", "2026-04-20", 
    "2026-04-21", "2026-04-22", "2026-04-23", "2026-04-24", "2026-04-27", 
    "2026-04-28", "2026-04-29", "2026-04-30", "2026-05-04", "2026-05-05", 
    "2026-05-06", "2026-05-07", "2026-05-08", "2026-05-11", "2026-05-12", 
    "2026-05-13", "2026-05-14", "2026-05-15", "2026-05-18", "2026-05-19"
]

closes = [
    1304.7, 1304.6, 1347.8, 1330, 1350.2, 1315.1, 1344.1, 1343.3, 1365, 1363.3,
    1353.3, 1362.1, 1343.4, 1327.8, 1365.8, 1388.9, 1425.4, 1430.8, 1463.1, 1463.6,
    1437.9, 1436.2, 1435.2, 1388.2, 1364, 1358.8, 1361.8, 1336.4, 1335.9, 1322.7
]

min_val = 1290
max_val = 1480
range_val = max_val - min_val

width = 650
height = 180

points = []
for i, val in enumerate(closes):
    x = i * (width / (len(closes) - 1))
    y = height - ((val - min_val) / range_val * height)
    points.append(f"{x},{y}")

points_str = " ".join(points)
polygon_points = f"0,{height} {points_str} {width},{height}"

html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    background-color: #171717;
    color: #e5e7eb;
    font-family: 'JetBrains Mono', monospace, sans-serif;
    margin: 0;
    padding: 16px;
    box-sizing: border-box;
    height: 100vh;
    border: 1px solid #262626;
    border-radius: 8px;
    overflow: hidden;
  }}
  .header {{
    font-size: 16px;
    font-weight: bold;
    color: #e5e7eb;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid #262626;
  }}
  .chart-container {{
    position: relative;
    width: {width}px;
    height: {height}px;
    margin-left: 40px;
    border-left: 1px solid #262626;
    border-bottom: 1px solid #262626;
  }}
  .y-label {{
    position: absolute;
    left: -40px;
    font-size: 12px;
    color: #737373;
  }}
  .top-label {{ top: -6px; }}
  .mid-label {{ top: calc(50% - 6px); }}
  .bot-label {{ bottom: -6px; }}
</style>
</head>
<body>
  <div class="header">PRICE HISTORY — RELIANCE.NS</div>
  
  <div class="chart-container">
    <div class="y-label top-label">₹1480</div>
    <div class="y-label mid-label">₹1385</div>
    <div class="y-label bot-label">₹1290</div>
    
    <svg width="{width}" height="{height}">
      <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:rgba(16, 185, 129, 0.4);" />
          <stop offset="100%" style="stop-color:rgba(16, 185, 129, 0.0);" />
        </linearGradient>
      </defs>
      
      <!-- Grid lines -->
      <line x1="0" y1="{height/2}" x2="{width}" y2="{height/2}" stroke="#262626" stroke-width="1" stroke-dasharray="4" />
      
      <!-- Area fill -->
      <polygon points="{polygon_points}" fill="url(#grad)" />
      
      <!-- Line -->
      <polyline points="{points_str}" fill="none" stroke="#10b981" stroke-width="2" />
    </svg>
  </div>
</body>
</html>
"""

with open(r'c:\Projects\signaldesk\.jetro\frames\pure_chart.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done")
