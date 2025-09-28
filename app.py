from flask import Flask, request, jsonify
from services.ocr import extract_text_pdf, ocr_pdf
from services.llm import llm_extract_items, llm_guess_ingredients, llm_guess_nutrients, llm_family_food_warning
from services.off_api import fetch_off_data
from services.risk import evaluate_risks
from db import save_extracted_items, save_bill_analysis, save_family_warnings
from flask import Flask, request, jsonify
from services.seasonal import get_seasonal_picks
# from services.expenses import get_expenses
from services.trends import get_price_trends
from services.nutrients import analyze_nutrient_gap
from services.meal_planner import generate_meal_plan
from db import save_family_details, save_family_warnings, save_bill_analysis

app = Flask(__name__)

@app.route("/upload-bill", methods=["POST"])
def upload_bill():
    file = request.files["file"]
    raw_text = extract_text_pdf(file) or ocr_pdf(file)
    items = llm_extract_items(raw_text)
    save_extracted_items(items)
    return jsonify({"items": items})

@app.route("/analyze-items", methods=["POST"])
def analyze_items():
    items = request.json.get("items", [])
    results = []
    for item in items:
        off_data = fetch_off_data(item["item_name"])
        llm_ing = llm_guess_ingredients(item["item_name"])
        llm_nut = llm_guess_nutrients(item["item_name"])
        risks = evaluate_risks(item, off_data, llm_ing, llm_nut)
        results.append({**item, **off_data, **llm_ing, **llm_nut, **risks})
    save_bill_analysis(results)
    return jsonify({"analysis": results})

@app.route("/family-warnings", methods=["POST"])
def family_warnings():
    family = request.json.get("family", [])
    items = request.json.get("items", [])
    warnings = llm_family_food_warning(items, family)
    save_family_warnings(warnings)
    return jsonify({"warnings": warnings})

@app.route("/seasonal-picks", methods=["GET"])
def seasonal_picks():
    location = request.args.get("location", "India")
    return jsonify(get_seasonal_picks(location))

# @app.route("/expenses", methods=["GET"])
# def expenses():
#     month = request.args.get("month")
#     year = request.args.get("year")
#     return jsonify(get_expense_summary(month, year))

@app.route("/price-trends", methods=["GET"])
def price_trends():
    item_name = request.args.get("item_name")
    return jsonify(get_price_trends(item_name))

@app.route("/nutrient-gap", methods=["POST"])
def nutrient_gap():
    data = request.json
    return jsonify(analyze_nutrient_gap(data.get("items", []), data.get("family", [])))

@app.route("/meal-planner", methods=["POST"])
def meal_planner():
    data = request.json
    return jsonify(generate_meal_plan(data.get("items", []), data.get("family", [])))

@app.route("/family-details", methods=["POST"])
def family_details():
    family = request.json
    save_family_details(family)
    return jsonify({"status": "saved"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
