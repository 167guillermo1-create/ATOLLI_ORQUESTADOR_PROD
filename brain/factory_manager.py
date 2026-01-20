import shutil
import os
import sys
import json
from datetime import datetime
from brain.design_system import DesignRegistry

class FactoryManager:
    """
    Universal Factory Engine for Atolli Nexus.
    Manages the creation, scaffolding, and orchestration of multi-platform ecosystems.
    """
    def __init__(self, factory_root="factory"):
        self.factory_root = os.path.abspath(factory_root)
        if not os.path.exists(self.factory_root):
            os.makedirs(self.factory_root)

    def create_ecosystem_scaffold(self, project_name, agent_orchestrator=None, schema_sql=None):
        """
        Creates the standard directory structure for a Nexus Trinity project.
        If 'NexusSeed' exists, it clones it; otherwise creates empty scaffold.
        """
        project_path = os.path.join(self.factory_root, project_name)
        seed_path = os.path.join(self.factory_root, "NexusSeed")
        
        if os.path.exists(project_path):
            raise Exception(f"Project '{project_name}' already exists.")

        created_paths = {}

        # CLONE STRATEGY (NexusSeed Prime)
        if os.path.exists(seed_path):
            print(f"🧬 Cloning from NexusSeed Prime...")
            shutil.copytree(seed_path, project_path)
            
            # Update internal references
            for root, dirs, files in os.walk(project_path):
                for d in dirs:
                    created_paths[d] = os.path.join(root, d)
            
            # Update Manifest
            manifest_path = os.path.join(project_path, "nexus_manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, "r") as f:
                    data = json.load(f)
                
                data["name"] = project_name
                data["created_at"] = str(datetime.now())
                data["parent_seed"] = "NexusSeed"
                
                with open(manifest_path, "w") as f:
                    json.dump(data, f, indent=4)
                    
        else:
            # FALLBACK STRATEGY (Empty Scaffold)
            print(f"⚠️ NexusSeed not found. Using fallback generation.")
            dirs = [
                "shared",        # SyncCore and common utilities
                "web_portal",    # Flet Web deployment
                "staff_app",     # Mobile (APK) and Desktop (EXE) app
                "data"           # Local databases and secrets
            ]
            
            if not os.path.exists(project_path):
                os.makedirs(project_path)
            
            for d in dirs:
                path = os.path.join(project_path, d)
                if not os.path.exists(path):
                    os.makedirs(path)
                created_paths[d] = path
                
            # Create an empty __init__.py in shared to allow imports
            with open(os.path.join(created_paths["shared"], "__init__.py"), "w") as f:
                pass
            
        if agent_orchestrator:
             self.provision_cloud_db(project_name, agent_orchestrator, schema_sql)
            
        return project_path, created_paths

    def inject_sync_core(self, target_shared_path):
        """
        Injects the standardized SyncCore template into the new project.
        """
        # Hardcoded template based on our professional standard (Aurora Sync 2026)
        sync_core_template = """import sqlite3
import json
import uuid
import time
import os
from datetime import datetime

class SyncCore:
    \"\"\"
    ATOLLI NEXUS SYNC-CORE (v1.1 - Phoenix)
    Handles offline-first persistence and cloud synchronization.
    \"\"\"
    def __init__(self, db_name="nexus_data.db"):
        self.db_path = os.path.join(os.getcwd(), "data", db_name)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Queue for pending changes
        cursor.execute('''CREATE TABLE IF NOT EXISTS sync_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT, 
            action TEXT, 
            payload TEXT, 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            synced INTEGER DEFAULT 0,
            retry_count INTEGER DEFAULT 0
        )''')
        # Local state storage
        cursor.execute('''CREATE TABLE IF NOT EXISTS local_state (
            key TEXT PRIMARY KEY,
            value TEXT
        )''')
        conn.commit()
        conn.close()

    def add_to_queue(self, table_name, action, payload):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sync_queue (table_name, action, payload) VALUES (?, ?, ?)",
                (table_name, action, json.dumps(payload))
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ [Sync-Core] Error adding to queue: {e}")
            return False

    def get_pending_sync(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sync_queue WHERE synced = 0 AND retry_count < 5")
            rows = cursor.fetchall()
            conn.close()
            return rows
        except:
            return []

    async def sync_to_supabase(self):
        \"\"\"
        Pulls pending items from the queue and attempts to push to Supabase.
        \"\"\"
        try:
            from .backend_manager import BackendManager
            backend = BackendManager()
            client = backend.get_client()
            if not client: return False
            
            pending = self.get_pending_sync()
            if not pending: return True
            
            for row in pending:
                id, table, action, payload, _, _, retry = row
                try:
                    data = json.loads(payload)
                    if action == "CREATE":
                        client.table(table).insert(data).execute()
                    elif action == "UPDATE":
                        # Logic for update depends on having an 'id' in data
                        pass
                        
                    # Update as synced
                    conn = sqlite3.connect(self.db_path)
                    conn.execute("UPDATE sync_queue SET synced = 1 WHERE id = ?", (id,))
                    conn.commit()
                    conn.close()
                except Exception as e:
                    print(f"❌ Sync Error (ID {id}): {e}")
                    conn = sqlite3.connect(self.db_path)
                    conn.execute("UPDATE sync_queue SET retry_count = retry_count + 1 WHERE id = ?", (id,))
                    conn.commit()
                    conn.close()
            return True
        except Exception as global_e:
            print(f"❌ Global Sync Error: {global_e}")
            return False
"""
        with open(os.path.join(target_shared_path, "sync_core.py"), "w", encoding="utf-8") as f:
            f.write(sync_core_template)
            
    def inject_backend_manager(self, target_shared_path):
        """
        Injects a standardized BackendManager to handle Supabase/Firebase connections.
        """
        backend_template = """import os
from dotenv import load_dotenv

class BackendManager:
    \"\"\"
    ATOLLI NEXUS BACKEND MANAGER
    Manages connections to Supabase or other cloud providers.
    \"\"\"
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.enabled = bool(self.url and self.key)

    def get_client(self):
        if not self.enabled:
            print("⚠️ Cloud Backend not configured.")
            return None
        # Dynamic import to avoid dependency issues if not used
        from supabase import create_client
        return create_client(self.url, self.key)
"""
        with open(os.path.join(target_shared_path, "backend_manager.py"), "w", encoding="utf-8") as f:
            f.write(backend_template)

    def prepare_trinity_manifest(self, project_path):
        """
        Generates a nexus_manifest.json to track the ecosystem components.
        """
        manifest = {
            "name": os.path.basename(project_path),
            "version": "1.0.0",
            "pillars": ["web", "android", "windows"],
            "backend": "supabase",
            "created_at": str(datetime.now())
        }
        with open(os.path.join(project_path, "nexus_manifest.json"), "w") as f:
            json.dump(manifest, f, indent=4)

    def inject_github_workflow(self, project_path):
        """
        Generates the standard GitHub Action for Nexus Trinity deployments.
        """
        nw_path = os.path.join(project_path, ".github", "workflows")
        if not os.path.exists(nw_path):
            os.makedirs(nw_path)
            
        workflow_content = """name: Nexus Trinity Build

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  trinity-build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install flet==0.80.2 supabase python-dotenv
      - name: Build Web
        run: flet build web web_portal/main.py
      - name: Build Windows EXE
        run: flet build windows staff_app/main.py --name "NexusApp"
      - name: Build Android APK
        run: flet build apk staff_app/main.py
      - name: Upload Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: trinity-binaries
          path: |
            build/web
            build/windows
            build/apk
"""
        with open(os.path.join(nw_path, "nexus_trinity.yml"), "w", encoding="utf-8") as f:
            f.write(workflow_content)

    def get_build_commands(self, project_path):
        """
        Returns the local CLI commands for packaging the ecosystem.
        """
        return {
            "windows": f"flet build windows {os.path.join('staff_app', 'main.py')}",
            "android": f"flet build apk {os.path.join('staff_app', 'main.py')}",
            "web": f"flet build web {os.path.join('web_portal', 'main.py')}"
        }

    def inject_design_tokens(self, target_shared_path, archetype="liquid_glass"):
        """
        Injects a design_tokens.py file based on the selected archetype.
        """
        token_code = DesignRegistry.get_token_code(archetype)
        with open(os.path.join(target_shared_path, "design_tokens.py"), "w", encoding="utf-8") as f:
            f.write(token_code)

    def inject_custom_logic(self, project_path, code):
        """
        Overwrites the primary main.py with custom AI-generated logic.
        """
        # Overwrite both web and staff app main files for consistency in this version
        targets = [
            os.path.join(project_path, "web_portal", "main.py"),
            os.path.join(project_path, "staff_app", "main.py")
        ]
        
        for target in targets:
            if os.path.exists(os.path.dirname(target)):
                with open(target, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"🧬 [Factory] Logic injected in: {target}")

    def provision_cloud_db(self, project_name, agent_orchestrator, schema_sql=None):
        """
        Uses the Agent's connection to Supabase to provision the cloud database.
        Chapter 2 - 'Invisible Data Engine'
        """
        if not agent_orchestrator or not agent_orchestrator.supabase:
            print("⚠️ Cloud DB Provisioning Skipped: Agent/Supabase not ready.")
            return False
            
        print(f"☁️ Provisioning Cloud Database for: {project_name}...")
        
        # Default Schema if none provided
        if not schema_sql:
            schema_sql = f"""
            -- Automatic Schema for {project_name}
            CREATE TABLE IF NOT EXISTS {project_name}_users (
                id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                username TEXT,
                email TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
            );
            
            ALTER TABLE {project_name}_users ENABLE ROW LEVEL SECURITY;
            CREATE POLICY "Public Access" ON {project_name}_users FOR ALL USING (true);
            """
            
        # Execute via RPC
        success = agent_orchestrator.supabase.execute_sql(schema_sql)
        if success:
            print(f"✅ Cloud Resources Provisioned for {project_name}")
        else:
            print(f"❌ Failed to Provision Cloud Resources.")
        
        return success

if __name__ == "__main__":
    # Test Scaffolding
    fm = FactoryManager()
    path, dirs = fm.create_ecosystem_scaffold("TestNexusProject")
    fm.inject_sync_core(dirs["shared"])
    print(f"Ecosystem created at: {path}")
