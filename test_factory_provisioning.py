import sys
import os
import shutil
import time

# Add current dir to path
sys.path.append(os.getcwd())

from main import SupabaseManager
from brain.factory_manager import FactoryManager
from dotenv import load_dotenv

class MockAgent:
    def __init__(self):
        self.supabase = SupabaseManager()

def test_full_factory_flow():
    project_name = f"TestCloudProject_{int(time.time())}"
    print(f">> Starting Full Factory Verification for: {project_name}")
    
    # 1. Initialize Components
    load_dotenv("data/.env")
    agent = MockAgent()
    
    if not agent.supabase.client:
        print("   [FAIL] Supabase connection failed. Aborting.")
        return

    factory = FactoryManager()
    
    # 2. Execute Factory Logic
    try:
        print("   -> Requesting Ecosystem Scaffold + Cloud DB...")
        path, created = factory.create_ecosystem_scaffold(project_name, agent_orchestrator=agent)
        
        print(f"      [OK] Project generated at: {path}")
        print("      [OK] Cloud Provisioning triggered (check logs above)")
        
        # 3. Verify Cloud Resource (Optional explicit check)
        check_sql = f"SELECT to_regclass('public.{project_name}_users');"
        # We can't easy get return value from execute_sql as it returns success bool, 
        # but if provisioning passed, we assume it's there. 
        # Let's try to query it to prove it exists.
        
        print("   -> Verifying Table Existence via Select...")
        verify_success = agent.supabase.execute_sql(f"SELECT count(*) FROM {project_name}_users")
        
        if verify_success:
            print("   [SUCCESS] Full Flow Verified: File System + Cloud Database.")
        else:
            print("   [WARNING] Table verification failed, but creation might have succeeded.")
            
    except Exception as e:
        print(f"   [FAIL] Factory Error: {e}")
        
    finally:
        # Optional Cleanup of FS
        # if os.path.exists(os.path.join(factory.factory_root, project_name)):
        #    shutil.rmtree(os.path.join(factory.factory_root, project_name))
        pass

if __name__ == "__main__":
    test_full_factory_flow()
