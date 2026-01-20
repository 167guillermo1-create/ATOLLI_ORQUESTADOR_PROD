import os
import sys
from brain.factory_manager import FactoryManager

def debug_scaffold():
    root = "C:/Users/Admin/Desktop/ATOLLI_ORQUESTADOR/Factory"
    project_name = "CineNexus"
    
    fm = FactoryManager(factory_root=root)
    project_path, paths = fm.create_ecosystem_scaffold(project_name)
    
    print(f"Project Path: {project_path}")
    for name, path in paths.items():
        print(f"Created {name} at: {path}")
        if os.path.exists(path):
            print(f"  [OK] Path exists")
        else:
            print(f"  [ERROR] Path does NOT exist")
            
    # Inject components
    fm.inject_sync_core(paths["shared"])
    fm.inject_backend_manager(paths["shared"])
    fm.inject_design_tokens(paths["shared"], archetype="liquid_glass")
    fm.prepare_trinity_manifest(project_path)
    fm.inject_github_workflow(project_path)
    
    print("Injection complete.")
    
    # List files to verify
    for root_dir, dirs, files in os.walk(project_path):
        for name in files:
            print(f"File: {os.path.join(root_dir, name)}")

if __name__ == "__main__":
    debug_scaffold()
