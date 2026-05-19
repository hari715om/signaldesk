"""
SignalDesk — FastAPI application.

Endpoints:
  GET  /health          → liveness check
  POST /analyze         → parallel analyst inference (real LLM)
  POST /analyze/mock    → hardcoded fake response (frontend dev / quota saving)
"""

import asyncio
import logging
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analysts import ANALYSTS
from groq_client import call_llm

logger = logging.getLogger("signaldesk.main")

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="SignalDesk API",
    description="AI investment committee — 4 analyst agents debate any stock in parallel.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class AnalyzeRequest(BaseModel):
    ticker: str
    question: str = "Should I invest in this stock?"


class AnalystResult(BaseModel):
    id: str
    name: str
    role: str
    color: str
    response: str
    score: int


class AnalyzeResponse(BaseModel):
    ticker: str
    analysts: list[AnalystResult]
    overall_sentiment: float
    verdict: str
    confidence: int


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_score(text: str, score_label: str) -> int:
    """
    Parse the analyst's self-reported score from their response.
    Falls back to 50 if the expected tag is missing or malformed.
    """
    pattern = rf"{re.escape(score_label)}:\s*(\d+)"
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        logger.warning("Score tag '%s' not found in response — defaulting to 50.", score_label)
        return 50
    return max(0, min(100, int(match.group(1))))


def _compute_verdict(overall: float) -> tuple[str, int]:
    """Return (verdict, confidence) from the composite sentiment score."""
    if overall >= 68:
        verdict = "BUY"
    elif overall >= 45:
        verdict = "HOLD"
    else:
        verdict = "SELL"

    confidence = int(overall)
    return verdict, confidence


async def _run_analyst(analyst: dict, user_message: str) -> AnalystResult:
    """Call the LLM for a single analyst and parse the result."""
    raw = await call_llm(analyst["system_prompt"], user_message)
    score = _extract_score(raw, analyst["score_label"])
    return AnalystResult(
        id=analyst["id"],
        name=analyst["name"],
        role=analyst["role"],
        color=analyst["color"],
        response=raw,
        score=score,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok", "analysts": len(ANALYSTS)}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    ticker = request.ticker.strip().upper()
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker cannot be empty.")

    user_message = f"Analyze {ticker}. Question: {request.question}"
    logger.info("Analyzing '%s' with %d analysts in parallel.", ticker, len(ANALYSTS))

    try:
        results: list[AnalystResult] = await asyncio.gather(
            *[_run_analyst(analyst, user_message) for analyst in ANALYSTS]
        )
    except Exception as exc:
        logger.error("Parallel inference failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {exc}. Check your API keys and try again.",
        )

    overall_sentiment = round(sum(r.score for r in results) / len(results), 1)
    verdict, confidence = _compute_verdict(overall_sentiment)

    return AnalyzeResponse(
        ticker=ticker,
        analysts=list(results),
        overall_sentiment=overall_sentiment,
        verdict=verdict,
        confidence=confidence,
    )


@app.post("/analyze/mock", response_model=AnalyzeResponse)
async def analyze_mock():
    """
    Returns a realistic hardcoded response for frontend development.
    Does NOT consume any API quota.
    """
    mock_analysts = [
        AnalystResult(
            id="bull",
            name="Alex Chen",
            role="Bull Analyst",
            color="#22c55e",
            score=74,
            response=(
                "DEMO's fundamentals tell a compelling growth story. Revenue has compounded at "
                "23% CAGR over three years, the TAM is expanding as enterprise adoption "
                "accelerates, and management has consistently beaten guidance. The balance sheet "
                "is clean with net cash. Margins are expanding 200–300 bps annually as operating "
                "leverage kicks in — a pattern typical of software businesses crossing the "
                "Rule-of-40 threshold. At current prices the risk/reward skews materially positive "
                "for a 2–3 year hold. Bull case: 60% upside if growth sustains at 20%+.\n\n"
                "CONFIDENCE: 74"
            ),
        ),
        AnalystResult(
            id="bear",
            name="Morgan Price",
            role="Bear Analyst",
            color="#ef4444",
            score=62,
            response=(
                "DEMO trades at 35x forward earnings — a 40% premium to sector peers with "
                "comparable growth profiles. Rising interest rates have already compressed "
                "multiples across high-duration assets, and DEMO is no exception. The latest "
                "quarter showed gross margin compression of 180 bps, which management attributed "
                "to 'investment mode' — a phrase that historically precedes estimate cuts. A new "
                "well-funded competitor entered the market last quarter. Bear case: 30% downside "
                "to fair value if growth decelerates even modestly to 15%.\n\n"
                "RISK: 62"
            ),
        ),
        AnalystResult(
            id="macro",
            name="Jordan Kim",
            role="Macro Analyst",
            color="#3b82f6",
            score=55,
            response=(
                "The macro backdrop is mixed for DEMO. The Fed's higher-for-longer posture "
                "continues to pressure growth-equity valuations via discount rate expansion — "
                "every 25 bps rate increase mechanically reduces DEMO's DCF fair value by "
                "roughly 4–5%. On the positive side, dollar weakness YTD benefits the "
                "international revenue segment (~30% of sales). Sector rotation data shows "
                "institutional money still cautious on tech vs. defensives. Geopolitically, "
                "DEMO's supply chain has limited China exposure, which reduces tail risk. "
                "Net: macro is a mild headwind, not a dealbreaker.\n\n"
                "MACRO: 55"
            ),
        ),
        AnalystResult(
            id="quant",
            name="Casey Okafor",
            role="Quant Analyst",
            color="#a855f7",
            score=68,
            response=(
                "Quantitative signals are constructive. P/E of 35x sits at the 55th percentile "
                "of the 5-year range (peak: 62x, trough: 18x) — not cheap, but not stretched. "
                "EV/EBITDA at 22x is in line with software peers. 3-month price momentum: +11%, "
                "6-month: +18%, 12-month: +27% — all above the sector median. Analyst estimate "
                "revisions are trending upward (+3 upgrades, 1 downgrade in the last 30 days). "
                "Short interest at 4.2% of float is low, limiting squeeze potential but also "
                "indicating limited institutional conviction against the name. Composite factor "
                "score: positive.\n\n"
                "QUANT: 68"
            ),
        ),
    ]

    scores = [r.score for r in mock_analysts]
    overall_sentiment = round(sum(scores) / len(scores), 1)
    verdict, confidence = _compute_verdict(overall_sentiment)

    return AnalyzeResponse(
        ticker="DEMO",
        analysts=mock_analysts,
        overall_sentiment=overall_sentiment,
        verdict=verdict,
        confidence=confidence,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
# Run with: uvicorn main:app --reload --port 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
