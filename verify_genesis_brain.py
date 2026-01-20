
import os
import sys
import time

# Add brain directory to path
sys.path.append(os.path.join(os.getcwd(), 'brain'))

# Mock Flet Page for main module import
import flet as ft
from unittest.mock import MagicMock

# Import AgentOrchestrator from main
# We need to handle the import carefully since main.py has a if __name__ == "__main__" block
# and global imports.
try:
    from main import AgentOrchestrator
except ImportError:
    # Try importing by path if local import fails
    sys.path.append(os.getcwd())
    from main import AgentOrchestrator

def test_brain():
    print("INICIANDO PROTOCOLO DE PRUEBA CEREBRAL...")
    
    env_path = os.path.join(os.getcwd(), "data", ".env")
    if not os.path.exists(env_path):
        print("❌ CRITICAL: No .env found in data/. Cannot test Brain without keys.")
        return

    agent = AgentOrchestrator(env_path)
    
    # 1. Check Prompt Loading
    if "Eres NEXUS MASTER GEN" in agent.system_prompt:
        print("✅ Prompt Maestro: DETECTADO")
    else:
        print("⚠️ Prompt Maestro: FALLBACK O MODIFICADO")
        print(f"   (Preview: {agent.system_prompt[:50]}...)")

    # 2. Check Connection Status
    print(f"🔌 Conectores: {list(agent.clients.keys())}")
    if not agent.clients:
        print("⚠️ WARNING: No AI clients configured. update data/.env")
        # cannot proceed with logic test
        return

    # 3. Test Reasoning & Healing
    prompt = "Genera un script de Python que imprima 'Hola Mundo' y explica brevemente."
    print(f"\nEnviando Prompt de Prueba: '{prompt}'")
    
    start = time.time()
    response = agent.process_request(prompt)
    duration = time.time() - start
    
    print(f"\nRESPUESTA ({duration:.2f}s):")
    print("-" * 40)
    print(response)
    print("-" * 40)
    
    # Validation
    if "Nexus Healer Scanned" in response:
        print("Firma del Healer: PRESENTE")
    else:
        # It's possible the LLM didn't generate code, so healer didn't trigger. 
        # But if we asked for a script, it should have.
        print("Firma del Healer: NO DETECTADA (¿Generó código?)")
        
    if "Auto-Corrected in Cycle" in response:
        print("Auto-Corrección: ACTIVADA (El ciclo funcionó)")
    
    print("\nPRUEBA CEREBRAL COMPLETADA.")

if __name__ == "__main__":
    test_brain()
