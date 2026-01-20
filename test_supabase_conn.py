import os
import sys
from dotenv import load_dotenv
import asyncio

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Windows Console Encoding Fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from supabase import create_client
except ImportError:
    print("❌ Error: supabase-py not installed. Run: pip install supabase")
    sys.exit(1)

def test_supabase():
    load_dotenv("data/.env")
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
        return

    print(f"Testing connection to: {url}")
    try:
        supabase = create_client(url, key)
        
        # Test 1: Check nexus_state table
        print("\n1. Testing 'nexus_state' table...")
        try:
            res = supabase.table("nexus_state").select("id").limit(1).execute()
            print("✅ 'nexus_state' table found and accessible.")
        except Exception as e:
            print(f"⚠️ 'nexus_state' test failed: {e}")
            print("   (Ensure you have run the SQL schema in brain/supabase_schema.sql)")

        # Test 2: Check usage_logs table
        print("\n2. Testing 'usage_logs' table...")
        try:
            res = supabase.table("usage_logs").select("id").limit(1).execute()
            print("✅ 'usage_logs' table found and accessible.")
        except Exception as e:
            print(f"⚠️ 'usage_logs' test failed: {e}")

        print("\n🚀 Supabase Test Complete.")
        
    except Exception as e:
        print(f"❌ Critical Connection Error: {e}")

if __name__ == "__main__":
    test_supabase()
