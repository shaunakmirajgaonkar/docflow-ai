"""
Local LLM wrapper around Ollama (https://ollama.com).

Install once, fully offline after model pull:
    ollama pull llama3.1
    ollama serve      # runs on http://localhost:11434 by default

This module never contacts any external API - every call is to 127.0.0.1.
"""
import json
import requests

from app.config import settings

OLLAMA_GENERATE_URL = f"{settings.OLLAMA_HOST}/api/generate"


def generate(prompt: str, system: str = "", temperature: float = 0.2, model: str = None) -> str:
    payload = {
        "model": model or settings.OLLAMA_MODEL,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {"temperature": temperature},
    }
    try:
        resp = requests.post(OLLAMA_GENERATE_URL, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not reach local Ollama at "
            f"{settings.OLLAMA_HOST}. Start it with `ollama serve` "
            f"and make sure `ollama pull {settings.OLLAMA_MODEL}` has been run."
        )


def generate_json(prompt: str, system: str = "", model: str = None) -> dict:
    """Ask the local model for strict JSON output and parse it defensively."""
    strict_system = (
        system
        + "\nRespond with ONLY valid JSON. No markdown fences, no commentary."
    )
    raw = generate(prompt, system=strict_system, temperature=0.0, model=model)
    raw = raw.strip().strip("`")
    if raw.lower().startswith("json"):
        raw = raw[4:].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(raw[start:end + 1])
            except json.JSONDecodeError:
                pass
        return {"raw_response": raw, "parse_error": True}
