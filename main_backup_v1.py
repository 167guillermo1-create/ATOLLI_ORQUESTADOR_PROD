import flet as ft
import os
import sys
from dotenv import load_dotenv

# Agregar path del brain
sys.path.append(os.path.join(os.path.dirname(__file__), "brain"))

try:
    from anchor import RealityAnchor, NexusHealer
    from factory_manager import FactoryManager
    from groq import Groq
except ImportError:
    print("WARNING: Brain modules or Groq not found")

class AgentOrchestrator:
    def __init__(self, env_path):
        self.env_path = env_path
        self.api_key = None
        self.client = None
        
        try:
            if os.path.exists(env_path):
                load_dotenv(env_path)
                self.api_key = os.getenv("GROQ_API_KEY")
                if self.api_key:
                    self.client = Groq(api_key=self.api_key)
                    print("🧠 CEREBRO ONLINE: Conectado a Groq Cloud")
                else:
                    print("⚠️ CEREBRO OFFLINE: Falta GROQ_API_KEY en .env")
        except Exception as e:
            print(f"❌ Error conectando cerebro: {e}")
            
        self.system_prompt = """Eres NEXUS MASTER GEN, el Arquitecto Jefe del sistema Atolli.
Tu objetivo es orquestar la creación de ecosistemas de software (Trinity).
ESTILO:
- Cyberpunk, técnico, conciso.
- Usa emojis técnicos (⚡, 🧬, 🛠️).
- Respuestas directas, sin relleno corporativo.
- Si te piden código, dalo optimizado.
- Tu creador es el Usuario (Admin).
"""

    def process_request(self, user_input):
        """Procesa solicitud del usuario vía LLM"""
        # Comandos locales rápidos
        if "/status" in user_input.lower():
            return "🟢 SISTEMA OPERACIONAL\n- Motor: Llama3-70b (bionic)\n- Factory: Ready"
        elif "/help" in user_input.lower():
            return "Comandos:\n/status - Estado del sistema\nCualquier otro texto: Chat con el Núcleo."
            
        # Chat con LLM
        if not self.client:
            return "⚠️ ERROR: Cerebro desconectado (No API Key). Verifica config."
            
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=500,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ ERROR NEURONAL: {str(e)}"

def main(page: ft.Page):
    # SETUP
    page.title = "NEXUS MASTER GEN"
    page.bgcolor = "#050505"
    page.padding = 20
    page.window_width = 1200
    page.window_height = 800
    page.update()
    
    NEON_CYAN = "#00f2ff"
    
    print("Sistema iniciado")
    
    # CHECK KNOWLEDGE BASE
    kb_path = os.path.join(os.getcwd(), "knowledge_base")
    if os.path.exists(kb_path):
        print(f"🧠 Knowledge Base Activa: {len(os.listdir(kb_path))} protocolos cargados.")
    else:
        print("⚠️ WARNING: Knowledge Base no detectada.")
    
    # BACKEND
    agent = None
    factory = None
    try:
        env_path = os.path.join(os.path.dirname(__file__), "data", ".env")
        agent = AgentOrchestrator(env_path)
        factory = FactoryManager("Factory")
        print("Backend conectado")
    except Exception as e:
        print(f"Backend error: {e}")
    
    # === MÓDULO BRAIN ===
    brain_chat = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=500)
    
    def add_message(text, sender="user"):
        msg = ft.Container(
            content=ft.Text(text, color="white", font_family="Consolas"),
            bgcolor="#003344" if sender == "user" else "#222222",
            padding=15,
            border_radius=10,
            border=ft.border.all(1, NEON_CYAN if sender == "user" else "transparent")
        )
        row = ft.Row([msg], alignment=ft.MainAxisAlignment.END if sender == "user" else ft.MainAxisAlignment.START)
        brain_chat.controls.append(row)
        page.update()
    
    def send_msg(e):
        if not brain_input.value: return
        text = brain_input.value
        brain_input.value = ""
        add_message(text, "user")
        
        if agent:
            try:
                response = agent.process_request(text)
                add_message(response, "agent")
            except Exception as ex:
                add_message(f"Error: {ex}", "agent")
        else:
            add_message("⚠️ Backend no disponible", "agent")
        
        brain_input.focus()
    
    brain_input = ft.TextField(
        hint_text="Escribe comando...",
        color="white",
        border_color=NEON_CYAN,
        text_style=ft.TextStyle(font_family="Consolas"),
        on_submit=send_msg,
        width=1000
    )
    
    brain_module = ft.Container(
        content=ft.Column([
            ft.Text("BRAIN - Chat IA", size=20, weight="bold", color=NEON_CYAN),
            ft.Divider(color="white24"),
            ft.Container(
                content=brain_chat,
                bgcolor="#0a0a0a",
                border=ft.border.all(1, "white12"),
                border_radius=10,
                padding=15,
                height=500
            ),
            ft.Row([brain_input, ft.ElevatedButton("ENVIAR", bgcolor=NEON_CYAN, color="black", on_click=send_msg)])
        ], spacing=10),
        visible=True,
        height=650
    )
    
    # === MÓDULO FACTORY ===
    factory_module = ft.Container(
        content=ft.Column([
            ft.Text("FACTORY - Generador Trinity", size=20, weight="bold", color=NEON_CYAN),
            ft.Divider(color="white24"),
            ft.Text("Selector de Arquetipos", color="white", size=16),
            ft.Row([
                ft.ElevatedButton("Liquid Glass", bgcolor="#1a1a1a", color="white"),
                ft.ElevatedButton("Bento", bgcolor="#1a1a1a", color="white"),
                ft.ElevatedButton("Minimal", bgcolor="#1a1a1a", color="white")
            ], spacing=10),
            ft.Container(height=20),
            ft.TextField(hint_text="Nombre del proyecto", color="white", width=400),
            ft.TextField(hint_text="Descripción", color="white", width=400, multiline=True, min_lines=3),
            ft.Container(height=20),
            ft.ElevatedButton("GENERAR PROYECTO", bgcolor=NEON_CYAN, color="black", width=200, on_click=lambda e: generate_project_handler(e))
        ], spacing=10),
        visible=False,
        height=650
    )
    
    def generate_project_handler(e):
        # Find the textfield at index 5 in the column (Name input)
        # Structure: Text, Divider, Text, Row, Container, TextField(Name), TextField(Desc), ...
        name_input = factory_module.content.controls[5]
        proj_name = name_input.value
        
        if not proj_name:
            add_message("⚠️ Error: El nombre del proyecto es obligatorio", "agent")
            return
            
        add_message(f"⚙️ Iniciando Protocolo Trinity para: {proj_name}...", "agent")
        
        try:
            if factory:
                path, _ = factory.create_ecosystem_scaffold(proj_name)
                add_message(f"✅ Proyecto generado exitosamente en:\n{path}", "agent")
                add_message("🧬 Clonado desde NexusSeed Prime (SyncCore v1.1)", "agent")
            else:
                 add_message("❌ Error Crítico: Factory Manager no conectado", "agent")
        except Exception as ex:
             add_message(f"❌ Error en generación: {ex}", "agent")
    
    # === MÓDULO MATRIX ===
    matrix_logs = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, height=500)
    
    matrix_module = ft.Container(
        content=ft.Column([
            ft.Text("MATRIX - Logs del Sistema", size=20, weight="bold", color=NEON_CYAN),
            ft.Divider(color="white24"),
            ft.Container(
                content=matrix_logs,
                bgcolor="#0a0a0a",
                border=ft.border.all(1, "white12"),
                border_radius=10,
                padding=15,
                height=500
            ),
            ft.ElevatedButton("LIMPIAR LOGS", bgcolor="#ff4444", color="white")
        ], spacing=10),
        visible=False,
        height=650
    )
    
    # === MÓDULO CONFIG ===
    config_module = ft.Container(
        content=ft.Column([
            ft.Text("CONFIG - Configuración", size=20, weight="bold", color=NEON_CYAN),
            ft.Divider(color="white24"),
            ft.Text("Credenciales (.env)", color="white", size=16),
            ft.TextField(hint_text="GROQ_API_KEY", color="white", width=500),
            ft.TextField(hint_text="SUPABASE_URL", color="white", width=500),
            ft.Container(height=20),
            ft.Text("Información del Sistema", color="white", size=16),
            ft.Text(f"Flet Version: 0.80.2", color="#888888"),
            ft.Text(f"Python: {sys.version.split()[0]}", color="#888888"),
            ft.Container(height=20),
            ft.ElevatedButton("GUARDAR CONFIGURACIÓN", bgcolor=NEON_CYAN, color="black", width=200)
        ], spacing=10),
        visible=False,
        height=650
    )
    
    # === NAVEGACIÓN ===
    active_tab = "brain"
    
    def switch_module(module_name):
        nonlocal active_tab
        active_tab = module_name
        
        brain_module.visible = (module_name == "brain")
        factory_module.visible = (module_name == "factory")
        matrix_module.visible = (module_name == "matrix")
        config_module.visible = (module_name == "config")
        
        # Actualizar colores de tabs
        brain_btn.bgcolor = NEON_CYAN if module_name == "brain" else "#1a1a1a"
        factory_btn.bgcolor = NEON_CYAN if module_name == "factory" else "#1a1a1a"
        matrix_btn.bgcolor = NEON_CYAN if module_name == "matrix" else "#1a1a1a"
        config_btn.bgcolor = NEON_CYAN if module_name == "config" else "#1a1a1a"
        
        brain_btn.color = "black" if module_name == "brain" else "white"
        factory_btn.color = "black" if module_name == "factory" else "white"
        matrix_btn.color = "black" if module_name == "matrix" else "white"
        config_btn.color = "black" if module_name == "config" else "white"
        
        page.update()
    
    brain_btn = ft.ElevatedButton("BRAIN", bgcolor=NEON_CYAN, color="black", on_click=lambda e: switch_module("brain"))
    factory_btn = ft.ElevatedButton("FACTORY", bgcolor="#1a1a1a", color="white", on_click=lambda e: switch_module("factory"))
    matrix_btn = ft.ElevatedButton("MATRIX", bgcolor="#1a1a1a", color="white", on_click=lambda e: switch_module("matrix"))
    config_btn = ft.ElevatedButton("CONFIG", bgcolor="#1a1a1a", color="white", on_click=lambda e: switch_module("config"))
    
    # === LAYOUT ===
    page.add(ft.Row([
        ft.Text("NEXUS MASTER GEN", size=24, weight="bold", color=NEON_CYAN),
        ft.Container(expand=True),
        ft.Text("ONLINE", color="green", size=14)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
    
    page.add(ft.Divider(color="white24"))
    
    page.add(ft.Row([brain_btn, factory_btn, matrix_btn, config_btn], spacing=10))
    
    page.add(ft.Divider(color="white24"))
    
    page.add(brain_module)
    page.add(factory_module)
    page.add(matrix_module)
    page.add(config_module)
    
    page.update()
    
    # Mensaje inicial
    add_message("Nexus Master Gen iniciado. Escribe /help para comandos.", "agent")
    print("Interfaz completa lista")

if __name__ == "__main__":
    print("=== NEXUS MASTER GEN ===")
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press ENTER...")
