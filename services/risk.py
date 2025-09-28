def evaluate_risks(item, off_data, llm_ing, llm_nut):
    risks = {}
    sugars = off_data.get("nutr_sugars_g") or llm_nut.get("nutr_sugars_g")
    if sugars and sugars > 15:
        risks["rule_severity"] = "High"
        risks["rule_reasons"] = "High sugar content"
    else:
        risks["rule_severity"] = "Low"
    return risks
