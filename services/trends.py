from db import supabase

def get_price_trends(item_name):
    data = supabase.table("bill_analysis") \
                   .select("item_name, price, purchase_date") \
                   .eq("item_name", item_name) \
                   .order("purchase_date", desc=True) \
                   .execute().data

    return {
        "item_name": item_name,
        "trends": [{"date": row["purchase_date"], "price": row["price"]} for row in data]
    }
