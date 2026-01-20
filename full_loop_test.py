import os
import sys
import json
import time
from dotenv import load_dotenv

# Asegurar que el path del proyecto esté disponible
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import AgentOrchestrator, SupabaseManager
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)

def run_full_loop_test():
    print("🚀 INICIANDO FULL LOOP TEST (BRAIN -> LOCAL -> CLOUD)")
    load_dotenv("data/.env")
    
    # 1. Inicializar Orchestrator
    # Usamos la ruta absoluta al .env
    env_path = os.path.abspath("data/.env")
    orchestrator = AgentOrchestrator(env_path)
    
    # 2. Guardar estado inicial
    initial_tokens = orchestrator.usage_stats['tokens_total']
    initial_cost = orchestrator.usage_stats['cost_usd']
    print(f"📊 Estado Inicial: {initial_tokens} tokens, ${initial_cost} USD")

    # 3. Simular interacción con el Brain
    test_prompt = "Hola Atolli, realiza una prueba de sincronización flash."
    print(f"💬 Enviando prompt al Brain: '{test_prompt}'")
    
    # Usamos Gemini como prueba por ser confiable en este entorno
    response = orchestrator.process_request(test_prompt)
    
    if "Error" in response:
        print(f"❌ Fallo en el Brain: {response}")
        return

    print(f"🤖 Respuesta recibida: {response[:50]}...")

    # 4. Verificar actualización local
    new_tokens = orchestrator.usage_stats['tokens_total']
    new_cost = orchestrator.usage_stats['cost_usd']
    print(f"📈 Estado Post-Interacción: {new_tokens} tokens, ${new_cost:.6f} USD")
    
    if new_tokens > initial_tokens:
        print("✅ Verificación Local: Éxito (Tokens incrementados).")
    else:
        print("❌ Verificación Local: Fallo (Tokens no incrementados).")

    # 5. Verificar sincronización en la nube (Supabase)
    print("☁️ Verificando sincronización en Supabase...")
    time.sleep(2) # Dar un momento para la escritura asíncrona (si la hubiera)
    
    try:
        # Consultar el último log en la tabla usage_logs
        res = orchestrator.supabase.client.table("usage_logs").select("*").order("timestamp", desc=True).limit(1).execute()
        
        if res.data:
            last_log = res.data[0]
            print(f"✅ Verificación Cloud: Éxito (Registro encontrado en Supabase).")
            print(f"   - Proveedor: {last_log['provider']}")
            print(f"   - Tokens: {last_log['tokens']}")
            print(f"   - Costo: ${last_log['cost_usd']}")
        else:
            print("❌ Verificación Cloud: Fallo (No se encontró el registro en Supabase).")
            
    except Exception as e:
        print(f"❌ Error al consultar Supabase: {e}")

    print("\n🏁 TEST COMPLETO.")

if __name__ == "__main__":
    run_full_loop_test()
