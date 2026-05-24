import json
import requests
from datetime import datetime
from django.conf import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

LANGUAGE_NAMES = {
    'ru': 'Russian',
    'uz': 'Uzbek',
    'en': 'English',
}


def _build_prompt(source, readings, language='en'):
    capacity = source.capacity_kw
    lang_name = LANGUAGE_NAMES.get(language, 'English')

    if readings:
        outputs = [r.output_kwh for r in readings]
        efficiencies = [r.efficiency_percent for r in readings if r.efficiency_percent]
        avg_output = round(sum(outputs) / len(outputs), 2)
        avg_efficiency = round(sum(efficiencies) / len(efficiencies), 2) if efficiencies else None
        max_output = round(max(outputs), 2)
        min_output = round(min(outputs), 2)
        recent = [
            {
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M"),
                "output_kwh": r.output_kwh,
                "efficiency_percent": r.efficiency_percent,
            }
            for r in readings[:5]
        ]
        perf_section = f"""Historical Performance (REAL DATA — base your numbers on this):
- Average Output: {avg_output} kWh
- Peak Output: {max_output} kWh
- Minimum Output: {min_output} kWh
- Average Efficiency: {avg_efficiency if avg_efficiency is not None else 'unknown'}%
- Number of Readings: {len(readings)}
- Recent Readings: {json.dumps(recent)}"""
    else:
        perf_section = """Historical Performance:
- No readings recorded yet. Estimate based on source type and capacity using realistic industry benchmarks.
- Typical capacity factors: solar 15-22%, wind 25-45%, hydro 35-60%, biomass 20-35%, geothermal 80-95%.
- Do NOT use 65% as a default — use the correct benchmark for the source type above."""

    return f"""You are an AI optimization engine for green energy systems. Analyze the following energy source and return a JSON optimization report.

IMPORTANT: Write the "recommendation" field and all strings inside "suggested_actions" in {lang_name} language only.

Energy Source:
- Name: {source.name}
- Type: {source.source_type}
- Installed Capacity: {capacity} kW
- Location: {source.location}
- Status: {source.status}

{perf_section}

Current time: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Respond ONLY with a valid JSON object. No explanation, no markdown, no backticks. Use exactly this structure:
{{
  "recommendation": "One clear actionable sentence in {lang_name}",
  "predicted_output_kwh": <realistic float based on capacity and source type>,
  "efficiency_score": <realistic float 0-100 based on actual data or type-specific benchmark, never hardcode 65>,
  "co2_saved_kg": <predicted_output_kwh * 0.233>,
  "confidence": <float 0.0-1.0, lower if no real readings>,
  "suggested_actions": ["action 1 in {lang_name}", "action 2 in {lang_name}", "action 3 in {lang_name}"],
  "trend": "improving" | "stable" | "declining"
}}"""


def run_optimization(source, readings, language='en'):
    api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
    model = getattr(settings, 'OPENROUTER_MODEL', 'deepseek/deepseek-chat')

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not set. Please add it as an environment variable in Render."
        )

    lang_name = LANGUAGE_NAMES.get(language, 'English')

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://greenai.onrender.com",
        "X-Title": "GreenAI Optimization System",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"You are a green energy AI optimization expert. "
                    f"You always respond with valid JSON only — no markdown, no explanation. "
                    f"Write all text values in {lang_name} language. "
                    f"Never hardcode efficiency as 65%; always use real data or type-specific benchmarks."
                ),
            },
            {
                "role": "user",
                "content": _build_prompt(source, readings, language),
            },
        ],
        "temperature": 0.3,
        "max_tokens": 600,
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("OpenRouter API request timed out.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"OpenRouter API error {e.response.status_code}: {e.response.text[:200]}"
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error: {str(e)}")

    data = response.json()
    try:
        raw_content = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected response format: {str(data)[:300]}")

    # Strip markdown fences if accidentally included
    if raw_content.startswith("```"):
        raw_content = raw_content.strip("`").strip()
        if raw_content.startswith("json"):
            raw_content = raw_content[4:].strip()

    try:
        result = json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Could not parse AI response as JSON: {str(e)}\nRaw: {raw_content[:300]}"
        )

    result["recommendation"] = str(result.get("recommendation", "No recommendation available."))
    result["predicted_output_kwh"] = float(result.get("predicted_output_kwh") or 0)
    result["efficiency_score"] = float(result.get("efficiency_score") or 0)
    result["co2_saved_kg"] = float(
        result.get("co2_saved_kg") or result["predicted_output_kwh"] * 0.233
    )
    result["confidence"] = min(1.0, max(0.0, float(result.get("confidence") or 0.7)))
    result["suggested_actions"] = list(result.get("suggested_actions") or [])
    result["trend"] = result.get("trend", "stable")
    result["source_type"] = source.source_type
    result["capacity_kw"] = source.capacity_kw
    result["generated_at"] = datetime.now().isoformat()
    result["model_used"] = model
    result["language"] = language
    return result
