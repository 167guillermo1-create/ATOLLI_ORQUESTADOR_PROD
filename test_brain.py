import os
import sys

# Mock Flet to avoid ImportError in main.py if we were to import it fully, 
# but here we only need AgentOrchestrator which mimics main.py logic.
# actually AgentOrchestrator is inside main.py, so we need to import it.
# To avoid running the UI code in main.py, we rely on the fact that main() is guarded by if __name__ == "__main__".

# We'll just copy the AgentOrchestrator logic here to test it in isolation OR import it if possible. 
# Importing main.py might trigger flet import. Let's try to import.
try:
    from main import AgentOrchestrator
except Exception as e:
    print(f"❌ CRITICAL IMPORT ERROR: {e}")
    # Force exit if we can't import the class under test
    sys.exit(1)

def test_brain():
    print("🧠 PRUEBA DE CONEXIÓN NEURONAL")
    
    env_path = os.path.join(os.getcwd(), "data", ".env")
    if not os.path.exists(env_path):
        print("❌ Error: .env no encontrado")
        return

    try:
        agent = AgentOrchestrator(env_path)
        if not agent.client:
            print("❌ Error: Cliente Groq no inicializado")
            return
            
        print("✅ Cliente Groq detectado.")
        
        prompt = "Hola, identifícate."
        print(f"🗣️ Enviando prompt: '{prompt}'")
        
        response = agent.process_request(prompt)
        print(f"🤖 Respuesta:\n{response}")
        
        if "NEXUS" in response or "Arquitecto" in response or "Atolli" in response:
            print("\n✅ PRUEBA EXITOSA: Personalidad confirmada.")
        else:
            print("\n⚠️ ALERTA: Respuesta genérica (Verificar System Prompt)")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

if __name__ == "__main__":
    test_brain()
