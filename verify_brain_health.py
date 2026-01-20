
import os
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

# Intentar cargar .env desde carpeta data
env_path = os.path.join(os.path.dirname(__file__), "data", ".env")
if os.path.exists(env_path):
    print(f"Cargando .env desde: {env_path}")
    load_dotenv(env_path, override=True)
else:
    print("⚠️ No se encontró data/.env, cargando variables de entorno del sistema.")

def test_groq():
    key = os.getenv("GROQ_API_KEY")
    if not key: return "SKIPPED (No Key)"
    try:
        from groq import Groq
        client = Groq(api_key=key)
        client.models.list()
        return "✅ ONLINE"
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

def test_deepseek():
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key: return "SKIPPED (No Key)"
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
        # Simple completion test
        client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1
        )
        return "✅ ONLINE"
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

def test_gemini():
    key = os.getenv("GEMINI_API_KEY")
    if not key: return "SKIPPED (No Key)"
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-pro')
        model.generate_content("ping")
        return "✅ ONLINE"
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

if __name__ == "__main__":
    print("="*40)
    print("🧠 BRAIN HEALTH DIAGNOSTIC")
    print("="*40)
    
    print(f"GROQ:     {test_groq()}")
    print(f"DEEPSEEK: {test_deepseek()}")
    print(f"GEMINI:   {test_gemini()}")
    
    print("="*40)
