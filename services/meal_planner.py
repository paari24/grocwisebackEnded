from services.llm import client, MODEL, _safe_json_parse

def generate_meal_plan(items, family):
    prompt = f"""
    Family: {family}
    Purchased items: {[i['item_name'] for i in items]}
    Create a 1-week meal plan with breakfast, lunch, dinner.
    Use purchased items as much as possible.
    Return JSON in format:
    {{
      "monday": {{"breakfast": "...", "lunch": "...", "dinner": "..."}},
      ...
    }}
    """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": "You are a meal planner."},
                  {"role": "user", "content": prompt}],
        temperature=0.6
    )
    return _safe_json_parse(resp.choices[0].message.content.strip())
