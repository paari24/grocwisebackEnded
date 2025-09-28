import requests

def fetch_off_data(item_name):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={item_name}&search_simple=1&action=process&json=1&page_size=1"
    r = requests.get(url)
    if r.status_code == 200 and r.json().get("products"):
        product = r.json()["products"][0]
        return {
            "product_name": product.get("product_name", ""),
            "ingredients_text": product.get("ingredients_text", ""),
            "nutriscore_grade": product.get("nutriscore_grade", ""),
            "nutr_energy_kcal": product.get("nutriments", {}).get("energy-kcal_100g", None),
            "nutr_protein_g": product.get("nutriments", {}).get("proteins_100g", None),
            "nutr_fat_g": product.get("nutriments", {}).get("fat_100g", None),
            "nutr_sugars_g": product.get("nutriments", {}).get("sugars_100g", None),
            "nutr_fiber_g": product.get("nutriments", {}).get("fiber_100g", None),
            "nutr_salt_g": product.get("nutriments", {}).get("salt_100g", None),
        }
    return {}
