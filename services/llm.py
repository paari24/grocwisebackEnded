from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


def _safe_json_parse(content: str):
    """
    Safely parse LLM output to JSON.
    Handles code fences like ```json ... ``` and extracts valid JSON.
    Falls back to extracting the first JSON array/object if extra text is present.
    """
    # Strip markdown code fences if present
    if content.startswith("```"):
        # remove leading/trailing fences
        content = content.strip().strip("`")
        # if it starts with 'json' keyword, strip it
        if content.lower().startswith("json"):
            content = content[4:].strip()
        # remove trailing ``` if still present
        if content.endswith("```"):
            content = content[:-3].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback: extract the first JSON object/array
        start = content.find("{")
        if start == -1:
            start = content.find("[")
        end = content.rfind("}") + 1 if "}" in content else content.rfind("]") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(content[start:end])
            except Exception:
                pass
        raise ValueError(f"Invalid JSON response from LLM after cleanup: {content}")


def llm_extract_items(raw_text):
    prompt = f"""
    You are analyzing OCR text from a grocery bill.
    Extract ONLY the purchased grocery food/ edible items with the brand name.
    do not include non-food items like toiletries, cleaning products, etc.
    brand name should not be generic like "Haldiram's Namkeen", it should be specific like "Haldiram's Aloo Bhujia".
    If quantity or pack size is not clear, set it to null. Give only edible items
    Ignore addresses, FSSAI, order numbers, invoice/tax info, totals.

    Return a JSON array. Each object must have:
    - item_name (string)
    - quantity (number if available, else null)
    - pack_size (string if available, else null)
    - price (number if available, else null)

    Bill text:
    
    {raw_text}
    """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a grocery bill parser. Output ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    content = resp.choices[0].message.content.strip()
    return _safe_json_parse(content)


def llm_guess_ingredients(item_name):
    prompt = f"""
    Guess ingredients for {item_name}.
    Return JSON in this format:
    {{
        "item_name": "{item_name}",
        "ingredients_text": "comma-separated ingredients"
    }}
    """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a food scientist. Output ONLY JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    content = resp.choices[0].message.content.strip()
    return _safe_json_parse(content)


def llm_guess_nutrients(item_name):
    prompt = f"""
    Estimate nutritional values for {item_name}.
    Return JSON with fields:
    {{
      "item_name": "{item_name}",
      "calories": float,
      "protein_g": float,
      "fat_g": float,
      "sugar_g": float,
      "salt_g": float
    }}
    """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a nutrition expert. Output ONLY JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    content = resp.choices[0].message.content.strip()
    return _safe_json_parse(content)


def llm_family_food_warning(items, family):
    prompt = f"""
    Family health risks: {family}
    Purchased items: {items}

    Suggest food warnings for each family member.
    Return JSON array in this format:
    [
      {{
        "member": "Name",
        "warning": "Reduce sugar intake due to diabetes"
      }}
    ]
    """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a health advisor. Output ONLY JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    content = resp.choices[0].message.content.strip()
    return _safe_json_parse(content)
