"""
SignalDesk — LLM client with Groq key rotation + Gemini fallback.

Strategy:
  1. Load all non-empty GROQ_KEY_* env vars into a round-robin cycle.
  2. On each call, grab the next key (thread-safe via Lock).
  3. On 429 / any HTTP error, try every remaining Groq key once.
  4. If all Groq keys are exhausted, fall back to Gemini 2.0 Flash.
  5. If Gemini also fails, raise a clear exception upstream.
"""

import asyncio
import itertools
import logging
import os
import threading

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("signaldesk.groq_client")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

# ---------------------------------------------------------------------------
# Key loading
# ---------------------------------------------------------------------------

def _load_groq_keys() -> list[str]:
    """Collect all non-empty GROQ_KEY_* values from environment."""
    keys = []
    for i in range(1, 10):  # supports up to GROQ_KEY_9
        key = os.getenv(f"GROQ_KEY_{i}", "").strip()
        if key:
            keys.append(key)
    if not keys:
        logger.warning("No GROQ_KEY_* env vars found — Groq calls will fail.")
    else:
        logger.info("Loaded %d Groq key(s).", len(keys))
    return keys


GROQ_KEYS: list[str] = _load_groq_keys()
GEMINI_KEY: str = os.getenv("GEMINI_KEY", "").strip()

# Round-robin cycle + lock for thread safety
_key_cycle = itertools.cycle(GROQ_KEYS) if GROQ_KEYS else iter([])
_cycle_lock = threading.Lock()


def _next_groq_key() -> str:
    """Return the next Groq key in the round-robin rotation."""
    with _cycle_lock:
        return next(_key_cycle)


# ---------------------------------------------------------------------------
# Groq call
# ---------------------------------------------------------------------------

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"


async def _call_groq(api_key: str, system_prompt: str, user_message: str) -> str:
    """Make a single async call to Groq. Raises httpx.HTTPStatusError on failure."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 300,
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(GROQ_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Gemini fallback
# ---------------------------------------------------------------------------

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)


async def _call_gemini(system_prompt: str, user_message: str) -> str:
    """Fallback to Google Gemini 2.0 Flash if all Groq keys fail."""
    if not GEMINI_KEY:
        raise RuntimeError("GEMINI_KEY is not set — no fallback available.")

    full_prompt = f"{system_prompt}\n\n{user_message}"
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
    params = {"key": GEMINI_KEY}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(GEMINI_URL, json=payload, params=params)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

async def call_llm(system_prompt: str, user_message: str) -> str:
    """
    Call an LLM with automatic Groq key rotation and Gemini fallback.

    Args:
        system_prompt: The analyst's full system prompt.
        user_message:  The user query (ticker + question).

    Returns:
        The raw text response from the model.

    Raises:
        RuntimeError: If every provider fails.
    """
    last_error: Exception | None = None

    # --- Try each Groq key once (full rotation) ---
    for attempt, _ in enumerate(GROQ_KEYS, start=1):
        key = _next_groq_key()
        masked = f"{key[:8]}…"
        logger.info("Groq attempt %d/%d — key %s", attempt, len(GROQ_KEYS), masked)
        try:
            result = await _call_groq(key, system_prompt, user_message)
            logger.info("Groq success on attempt %d.", attempt)
            return result
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            logger.warning("Groq key %s returned HTTP %d.", masked, status)
            last_error = exc
        except Exception as exc:  # network errors, timeouts, etc.
            logger.warning("Groq key %s error: %s", masked, exc)
            last_error = exc

    # --- All Groq keys failed — try Gemini ---
    logger.warning("All Groq keys failed. Falling back to Gemini 2.0 Flash.")
    try:
        result = await _call_gemini(system_prompt, user_message)
        logger.info("Gemini fallback succeeded.")
        return result
    except Exception as exc:
        logger.error("Gemini fallback also failed: %s", exc)
        last_error = exc

    raise RuntimeError(
        f"All LLM providers failed. Last error: {last_error}"
    )
