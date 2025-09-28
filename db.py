from supabase import create_client
import os
from dotenv import load_dotenv
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def save_extracted_items(items):
    for item in items:
        supabase.table("extracted_items").insert(item).execute()

def save_bill_analysis(results):
    supabase.table("bill_analysis").insert(results).execute()

def save_family_warnings(warnings):
    supabase.table("family_warnings").insert(warnings).execute()

def save_family_details(family):
    supabase.table("family_details").insert(family).execute()

def save_extracted_items(items):
    for item in items:
        supabase.table("extracted_items").insert(item).execute()


def save_bill_analysis(results):
    supabase.table("bill_analysis").insert(results).execute()


def save_family_warnings(warnings):
    supabase.table("family_warnings").insert(warnings).execute()