# services/seasonal.py
from services.llm import client, _safe_json_parse, MODEL


def get_seasonal_picks(location: str):
    prompt = f"""
    Suggest seasonal and budget-friendly grocery items for location: {location}.
    Return JSON array with fields:
    - item_name (string)
    - season (string, e.g., Summer, Winter)
    - avg_price (float, INR)
    """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a grocery market analyst. Output ONLY JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return _safe_json_parse(resp.choices[0].message.content.strip())
