import requests
import os
import sys
from dotenv import load_dotenv

def flush(msg):
    print(msg)
    sys.stdout.flush()

def diag():
    flush("=== SUPABASE DIAGNOSTIC START ===")
    load_dotenv("data/.env")
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        flush("❌ ERROR: Missing URL or KEY in .env")
        return

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    test_tables = ["nexus_state", "usage_logs"]
    
    for table in test_tables:
        flush(f"Checking table: {table}...")
        api_url = f"{url}/rest/v1/{table}?select=*&limit=1"
        try:
            response = requests.get(api_url, headers=headers)
            flush(f"Response Code: {response.status_code}")
            if response.status_code == 200:
                flush(f"✅ Table '{table}' exists and is accessible.")
            elif response.status_code == 404:
                flush(f"❌ Table '{table}' DOES NOT EXIST (404).")
            else:
                flush(f"⚠️ Unexpected status for '{table}': {response.status_code}")
                flush(f"Body: {response.text}")
        except Exception as e:
            flush(f"❌ Request failed for '{table}': {e}")

    flush("=== SUPABASE DIAGNOSTIC END ===")

if __name__ == "__main__":
    diag()
