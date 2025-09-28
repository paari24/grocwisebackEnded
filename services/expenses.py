# from services.llm import client, _safe_json_parse, MODEL

# def get_expense_summary(items, month, year):
#     prompt = f"""
#     Given these purchased items: {items}
#     Summarize expenses for {month}/{year}.
#     Return JSON:
#     {{
#       "month": "{month}",
#       "year": "{year}",
#       "total_expense": float,
#       "category_breakdown": [
#         {{"category": "Beverages", "amount": float}},
#         {{"category": "Snacks", "amount": float}}
#       ]
#     }}
#     """
#     resp = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": "You are an expense analyzer. Output ONLY JSON."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.3
#     )
#     return _safe_json_parse(resp.choices[0].message.content.strip())
