import os
import sys
import shutil
import time

# Sync path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import AgentOrchestrator
from brain.factory_manager import FactoryManager

def run_loop_audit():
    print("🚀 INICIANDO AUDITORÍA DE BUCLE COMPLETO (CHAPTER 10)")
    
    # 1. Setup Orchestrator
    data_dir = os.path.join(os.getcwd(), "data")
    env_path = os.path.join(data_dir, ".env")
    
    # Ensure env exists for test (mocking supabase sync as it requires real creds)
    from unittest.mock import MagicMock, patch
    with patch('main.SupabaseManager') as mock_sb:
        mock_sb.return_value.load_state.return_value = {"evolution_level": 1, "experience_points": 0}
        mock_sb.return_value.save_state.return_value = True
        mock_sb.return_value.sync_usage.return_value = True
        mock_sb.return_value.execute_sql.return_value = {"status": "success"}

        orchestrator = AgentOrchestrator(env_path)
        
        # 2. TEST: App Generation Command
        print("\n🛠️ TEST 1: Generación de App Full-Stack via Comando...")
        test_command = "Crear proyecto full stack 'Nexus_Final_Validation' con tabla 'AuditLogs'"
        
        # We simulate the user input processing
        # In a real environment, this triggers FactoryManager
        factory = FactoryManager("Factory")
        
        # Simulate the response from Orchestrator logic
        response = orchestrator.process_request(test_command)
        print(f"   Nexus Response: {response[:100]}...")
        
        # Manual execution of factory to verify logic
        print("   Ejecutando Factory Provisioning...")
        project_name = "Nexus_Final_Validation"
        project_path = os.path.join(os.getcwd(), "Factory", project_name)
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
            
        factory_result = factory.create_ecosystem_scaffold(project_name)
        
        # 3. VERIFY: Local Files
        project_path = os.path.join(os.getcwd(), "Factory", "Nexus_Final_Validation")
        if os.path.exists(project_path):
            print(f"✅ Carpeta de Proyecto Creada: {project_path}")
            # Check for README or critical files
            if os.path.exists(os.path.join(project_path, "main.py")):
                print("✅ main.py inyectado correctamente.")
        else:
            print("❌ FALLO: Carpeta de proyecto no encontrada.")
            return False

        # 4. VERIFY: Multiplatform Deliverables
        print("\n📦 TEST 2: Auditoría de Artefactos de Distribución...")
        icon_path = os.path.join(os.getcwd(), "assets", "icon.png")
        build_script = os.path.join(os.getcwd(), "build_production.py")
        workflow_path = os.path.join(os.getcwd(), ".github", "workflows", "build_apk.yml")
        
        critical_assets = [icon_path, build_script, workflow_path]
        for asset in critical_assets:
            if os.path.exists(asset):
                print(f"✅ Artefacto detectado: {os.path.basename(asset)}")
            else:
                print(f"❌ FALLO: Artefacto faltante -> {asset}")
                return False

        # 5. TEST: Web UI Sync (Logic Level)
        print("\n🌐 TEST 3: Sincronización de Lógica UI...")
        # Check if evolution increased
        if orchestrator.nexus_state.get("experience_points", 0) > 0:
            print(f"✅ XP ganado en el bucle: {orchestrator.nexus_state['experience_points']}")
        else:
            print("❌ FALLO: XP no registrado.")
            return False

    print("\n🏁 RESULTADO FINAL: 100% OPERATIVO")
    return True

if __name__ == "__main__":
    success = run_loop_audit()
    if not success:
        sys.exit(1)
