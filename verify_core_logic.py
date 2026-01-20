import os
import sys
import json
from dotenv import load_dotenv

# Ensure path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import AgentOrchestrator
from brain.factory_manager import FactoryManager
from brain.design_system import DesignRegistry

def run_tests():
    print("🔬 INICIANDO VERIFICACIÓN DE LÓGICA CORE (BACKEND)")
    
    # SETUP
    env_path = os.path.abspath("data/.env")
    orchestrator = AgentOrchestrator(env_path)
    factory = FactoryManager("FactoryMain")
    
    # TEST 1: CONFIG & API KEYS
    print("\n[1] Probando Gestión de Configuración...")
    orchestrator.reload_config()
    print(f"   - API Keys cargadas: {[k for k,v in {'Groq': orchestrator.groq_key, 'DeepSeek': orchestrator.deepseek_key, 'Gemini': orchestrator.gemini_key}.items() if v]}")
    
    if hasattr(orchestrator, 'usage_stats'):
        print(f"   - Estadísticas de uso accesibles: {list(orchestrator.usage_stats.keys())}")
    else:
        print("   ❌ ERROR: usage_stats no inicializado.")

    # TEST 2: FACTORY MODULE
    print("\n[2] Probando Módulo Factory...")
    if hasattr(factory, 'create_ecosystem_scaffold'):
        print("   ✅ FactoryManager: Método 'create_ecosystem_scaffold' disponible.")
    else:
        print("   ❌ FactoryManager: Método Crítico NO disponible.")

    # Check Design Templates via Registry
    print("\n[2.1] Probando Templates de Diseño...")
    templates = list(DesignRegistry.ARCHETYPES.keys())
    print(f"   - Arquetipos UI disponibles: {templates}")
        
    # TEST 3: DESIGN SYSTEM REGISTRY
    print("\n[3] Probando Design System...")
    aurora = DesignRegistry.ARCHETYPES.get("aurora_glass")
    if aurora and aurora.get("blur") == 30:
        print("   ✅ Aurora Glass Tokens correctos.")
    else:
        print("   ❌ ERROR: Tokens de diseño corruptos.")

    # TEST 4: SUPABASE CONNECTION
    print("\n[4] Probando Conexión Supabase (Ping)...")
    try:
        print(f"   - URL: {orchestrator.supabase.url}")
        print(f"   - Key Loaded: {'Yes' if orchestrator.supabase.key else 'No'}")
        print(f"   - Client Object: {orchestrator.supabase.client}")
        
        if orchestrator.supabase.client:
            orchestrator.supabase.client.table("nexus_state").select("id").limit(1).execute()
            print("   ✅ Conexión Supabase ACTIVA.")
        else:
             print("   ❌ ERROR: Cliente Supabase es None.")
    except Exception as e:
         print(f"   ❌ ERROR Supabase: {e}")

    print("\n🏁 VERIFICACIÓN LÓGICA COMPLETADA.")

if __name__ == "__main__":
    run_tests()
