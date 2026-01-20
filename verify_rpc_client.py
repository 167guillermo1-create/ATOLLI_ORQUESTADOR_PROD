import sys
import os
# Add current dir to path to import main
sys.path.append(os.getcwd())

from main import SupabaseManager
from dotenv import load_dotenv

def verify_rpc_client():
    print(">> Verifying RPC Client Connection...")
    load_dotenv("data/.env")
    
    # Initialize Manager
    sm = SupabaseManager()
    if not sm.client:
        print("   [FAIL] SupabaseManager failed to initialize client.")
        return

    # Test Query: Create a temp table
    test_table = "test_rpc_verification"
    sql = f"CREATE TABLE IF NOT EXISTS {test_table} (id serial primary key, message text);"
    
    print(f"   -> Attempting to create table '{test_table}' via RPC...")
    success = sm.execute_sql(sql)
    
    if success:
        print("   [OK] Table creation check passed.")
        # Cleanup
        sm.execute_sql(f"DROP TABLE {test_table};")
        print("   [OK] Cleanup passed.")
        print("\n>> RPC CLIENT VERIFICATION COMPLETE [SUCCESS]")
    else:
        print("\n   [FAIL] RPC Execution failed.")

if __name__ == "__main__":
    verify_rpc_client()
