"""
Script de Prueba del Trinity Protocol
Genera un proyecto de prueba para verificar el funcionamiento completo del sistema
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "brain"))

from factory_manager import FactoryManager
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

# Cargar configuración
load_dotenv()

print("=" * 60)
print("PRUEBA DEL TRINITY PROTOCOL")
print("=" * 60)

# Configuración del proyecto de prueba
PROJECT_NAME = "TestCalculator"
PROJECT_DESC = "Calculadora científica con diseño moderno y funciones básicas"
ARCHETYPE = "liquid_glass"

print(f"\n📋 Proyecto: {PROJECT_NAME}")
print(f"📝 Descripción: {PROJECT_DESC}")
print(f"🎨 Arquitectura: {ARCHETYPE}")

# Fase 1: Inicializar Factory Manager
print("\n" + "=" * 60)
print("FASE 1: INICIALIZACIÓN")
print("=" * 60)

factory = FactoryManager()
print("✅ Factory Manager inicializado")

# Fase 2: Crear Scaffold
print("\n" + "=" * 60)
print("FASE 2: SCAFFOLD (Estructura Base)")
print("=" * 60)

project_path, created_paths = factory.create_ecosystem_scaffold(PROJECT_NAME)
print(f"✅ Scaffold creado en: {project_path}")

# Verificar estructura
expected_dirs = [
    os.path.join(project_path, "web_portal"),
    os.path.join(project_path, "staff_app"),
    os.path.join(project_path, "shared"),
]

for dir_path in expected_dirs:
    if os.path.exists(dir_path):
        print(f"  ✅ {os.path.basename(dir_path)}/")
    else:
        print(f"  ❌ {os.path.basename(dir_path)}/ NO ENCONTRADO")

# Fase 3: Generación de Código AI
print("\n" + "=" * 60)
print("FASE 3: GENERACIÓN DE CÓDIGO AI")
print("=" * 60)

# Configurar Gemini
gemini_key = os.getenv("GEMINI_API_KEY")
deepseek_key = os.getenv("DEEPSEEK_API_KEY")

ai_code = None

if gemini_key:
    try:
        print("🔄 Intentando con Gemini...")
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
ACT AS: Senior Flet Developer.
GOAL: Create a high-end 'main.py' for a staff application component of a Trinity Ecosystem.
PROJECT: {PROJECT_NAME}
DESCRIPTION: {PROJECT_DESC}
ARCHETYPE: {ARCHETYPE}

REQUIREMENTS:
1. Use 'from shared.design_tokens import ACCENT_COLOR, BORDER_RADIUS, get_glass_style' for styling.
2. Use 'from shared.sync_core import SyncCore' for data persistence.
3. The UI must be professional, dark mode, and responsive.
4. Include at least 2 functional features based on the description.
5. DO NOT include external assets like local images unless they are standard icons.
6. Return ONLY the Python code, no markdown blocks, no explanations.
"""
        
        response = model.generate_content(prompt)
        ai_code = response.text.replace("```python", "").replace("```", "").strip()
        print("✅ Código generado por Gemini")
        print(f"📊 Tamaño del código: {len(ai_code)} caracteres")
        
    except Exception as e:
        print(f"⚠️ Error con Gemini: {e}")

# Fallback a DeepSeek
if not ai_code and deepseek_key:
    try:
        print("🔄 Intentando con DeepSeek...")
        client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
        
        prompt = f"""
ACT AS: Senior Flet Developer.
GOAL: Create a high-end 'main.py' for a staff application.
PROJECT: {PROJECT_NAME}
DESCRIPTION: {PROJECT_DESC}

Create a professional Flet app with dark mode, responsive design, and at least 2 features.
Use 'from shared.design_tokens import ACCENT_COLOR, BORDER_RADIUS, get_glass_style'.
Return ONLY Python code, no markdown.
"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_code = response.choices[0].message.content.replace("```python", "").replace("```", "").strip()
        print("✅ Código generado por DeepSeek")
        print(f"📊 Tamaño del código: {len(ai_code)} caracteres")
        
    except Exception as e:
        print(f"⚠️ Error con DeepSeek: {e}")

# Fase 4: Inyección de Código
if ai_code:
    print("\n" + "=" * 60)
    print("FASE 4: INYECCIÓN DE CÓDIGO")
    print("=" * 60)
    
    factory.inject_custom_logic(project_path, ai_code)
    print("✅ Código AI inyectado en web_portal/main.py y staff_app/main.py")
    
    # Verificar inyección
    staff_main = os.path.join(project_path, "staff_app", "main.py")
    if os.path.exists(staff_main):
        with open(staff_main, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content) > 500:  # Verificar que no sea solo boilerplate
                print(f"✅ Archivo staff_app/main.py actualizado ({len(content)} caracteres)")
            else:
                print("⚠️ El archivo parece muy pequeño, posible error en inyección")
else:
    print("\n❌ No se pudo generar código AI. Usando boilerplate estándar.")

# Fase 5: Verificación Final
print("\n" + "=" * 60)
print("FASE 5: VERIFICACIÓN FINAL")
print("=" * 60)

# Verificar archivos clave
key_files = [
    "web_portal/main.py",
    "staff_app/main.py",
    "shared/sync_core.py",
    "shared/backend_manager.py",
    "shared/design_tokens.py",
    "web_portal/requirements.txt",
    "staff_app/requirements.txt",
]

all_ok = True
for file_rel in key_files:
    file_path = os.path.join(project_path, file_rel)
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"  ✅ {file_rel} ({size} bytes)")
    else:
        print(f"  ❌ {file_rel} NO ENCONTRADO")
        all_ok = False

# Resumen
print("\n" + "=" * 60)
print("RESUMEN DEL TRINITY PROTOCOL")
print("=" * 60)

if all_ok and ai_code:
    print("✅ TRINITY PROTOCOL COMPLETADO EXITOSAMENTE")
    print(f"\n📁 Proyecto generado en:")
    print(f"   {project_path}")
    print(f"\n🚀 Próximos pasos:")
    print(f"   1. cd {project_path}/staff_app")
    print(f"   2. pip install -r requirements.txt")
    print(f"   3. flet run main.py")
elif all_ok:
    print("⚠️ TRINITY PROTOCOL COMPLETADO CON ADVERTENCIAS")
    print("   - Estructura creada correctamente")
    print("   - Código AI no generado (usando boilerplate)")
else:
    print("❌ TRINITY PROTOCOL INCOMPLETO")
    print("   - Algunos archivos no se generaron correctamente")

print("\n" + "=" * 60)
