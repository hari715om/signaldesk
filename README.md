# SignalDesk — AI Investment Committee Workspace

> Four specialized AI analyst agents debate any stock in parallel. Get a Bull, Bear, Macro, and Quant perspective in under 3 seconds.

---

## What it does

A user types any stock ticker. Four AI analyst agents — each with a completely different reasoning style, cognitive bias, and intentional blind spot — analyze the stock simultaneously via `asyncio.gather()`. Their outputs appear as styled cards in a dark terminal-style UI. A consensus meter shows each analyst's sentiment score as an animated bar. A final verdict card renders **BUY / HOLD / SELL** with a confidence percentage.

The workspace lives on a Jetro canvas that can be annotated and shared as a public URL.

---

## Demo

🔗 **Live Canvas:** [Jetro public URL — add after Phase 3 setup]

![SignalDesk Main View](screenshots/signaldesk-main.png)

---

## Architecture

```
User types ticker
     ↓
React UI (localhost:5173)
     ↓
FastAPI backend (localhost:8000)
     ↓  asyncio.gather() — fires all 4 simultaneously
┌────────┬────────┬─────────┬──────────┐
│  Bull  │  Bear  │  Macro  │  Quant   │
│  Alex  │ Morgan │ Jordan  │  Casey   │
│ (Groq) │ (Groq) │ (Groq)  │  (Groq)  │
└────────┴────────┴─────────┴──────────┘
     ↓
Score extraction via regex + consensus averaging
     ↓
BUY / HOLD / SELL verdict
     ↓
Jetro canvas (annotatable, shareable workspace)
```

---

## Features

- **4 specialized analyst agents** with distinct reasoning styles and intentional blind spots — engineered to disagree
- **Genuine parallel inference** via `asyncio.gather()` — all 4 analysts respond simultaneously, total latency < 3s
- **Multi-key Groq rotation** — round-robin across up to 3 free API keys, thread-safe; automatic Gemini 2.0 Flash fallback
- **Animated consensus meter** — per-analyst sentiment bars animate on render
- **Typewriter streaming effect** on analyst responses — 12ms per character
- **Score count-up animation** — circular score badge counts up from 0 on mount
- **Dark Bloomberg-terminal UI** — JetBrains Mono, `#0a0a0a` background, per-analyst accent colors
- **Skeleton loader** — shimmer placeholder cards while inference runs
- **Mock endpoint** — `/analyze/mock` returns hardcoded data for frontend dev without burning quota
- **Jetro canvas integration** — workspace is annotatable, loggable, shareable as a public URL

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite |
| Backend | FastAPI + Python 3.11 |
| AI Inference | Groq (`llama-3.3-70b-versatile`) |
| AI Fallback | Google Gemini 2.0 Flash |
| Canvas | Jetro |
| Editor | Antigravity |

---

## Setup

### Prerequisites

- Python 3.11+
- Node 18+
- Free Groq API key from [console.groq.com](https://console.groq.com) — create 3 accounts for 3× free quota
- Optional: Google AI Studio key from [aistudio.google.com](https://aistudio.google.com) for fallback

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp ../.env.example .env    # then fill in your actual keys
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**

### 3. Test the backend directly

```powershell
# Windows PowerShell
Invoke-RestMethod -Method POST -Uri http://localhost:8000/analyze `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"ticker": "NVDA", "question": "Should I invest?"}'

# macOS/Linux
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA", "question": "Should I invest?"}'
```

---

## Analyst Design

See [docs/system-prompts.md](docs/system-prompts.md) for the full prompt design rationale.

| Analyst | Persona | Scores | Deliberately Ignores |
|---|---|---|---|
| **Alex Chen** | Bull Analyst | CONFIDENCE 0–100 | Valuation stretch |
| **Morgan Price** | Bear Analyst | RISK 0–100 | Growth potential |
| **Jordan Kim** | Macro Analyst | MACRO 0–100 | Company-level fundamentals |
| **Casey Okafor** | Quant Analyst | QUANT 0–100 | Narrative context |

---

## Verdict Logic

| Score Range | Verdict |
|---|---|
| ≥ 68 | **BUY** |
| 45–67 | **HOLD** |
| < 45 | **SELL** |

Overall score = simple average of all 4 analyst scores. The score labels are intentionally asymmetric: Bull's CONFIDENCE and Bear's RISK both point in opposite directions, which creates genuine tension in the aggregate.

---

## What I Learned Building This

Parallel LLM inference with `asyncio.gather()` is surprisingly clean — the complexity isn't in the concurrency, it's in the prompt engineering. Getting four agents to *genuinely disagree* rather than produce surface-level variation required giving each one explicit cognitive constraints: Bull ignores valuation, Bear ignores growth, Macro ignores fundamentals, Quant ignores narrative. Without those constraints, all four agents converge on the same hedge-everything response.

The Jetro canvas layer turned a demo into a workspace — the embed + notes panel + session log transforms a single-use API call into something you'd actually return to.

---

## License

MIT

---

*Built for Berrywise internship submission | May 2025 | Hari om Singh*
