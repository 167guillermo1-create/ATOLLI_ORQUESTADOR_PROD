import flet as ft
import os
import sys
from dotenv import load_dotenv
import json
from supabase import create_client, Client

sys.stdout.reconfigure(encoding='utf-8')

# Agregar path del brain
sys.path.append(os.path.join(os.path.dirname(__file__), "brain"))

# SDK Disponibilidad
SDK_MODELS = {
    'groq': False,
    'genai': False,
    'openai': False
}

try:
    from anchor import RealityAnchor, NexusHealer
    from factory_manager import FactoryManager
    from design_system import DesignRegistry, ResponsiveScanner
    from ui_components import GlassInput, LuxuryStepper, SmartTooltip
except ImportError:
    print("WARNING: Local brain modules not found")

try:
    from groq import Groq
    SDK_MODELS['groq'] = True
except ImportError: print("SDK Groq missing")

try:
    import google.generativeai as genai
    SDK_MODELS['genai'] = True
except ImportError: print("SDK Gemini missing")

try:
    from openai import OpenAI
    SDK_MODELS['openai'] = True
except ImportError: print("SDK OpenAI/DeepSeek missing")

class SupabaseManager:
    """Maneja la persistencia en la nube vía Supabase."""
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client = None
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
            except Exception as e:
                print(f"Error initializing Supabase: {e}")

    def save_state(self, state_data):
        """Guarda el estado en la tabla 'nexus_state'."""
        if not self.client: return False
        try:
            data = {"id": 1, "data": state_data, "updated_at": "now()"}
            self.client.table("nexus_state").upsert(data).execute()
            return True
        except Exception as e:
            print(f"☁️ Supabase Save Error (State): {e}")
            return False

    def load_state(self):
        """Carga el estado desde Supabase."""
        if not self.client: return None
        try:
            response = self.client.table("nexus_state").select("data").eq("id", 1).execute()
            if response.data:
                return response.data[0]["data"]
        except Exception as e:
            print(f"☁️ Supabase Load Error: {e}")
        return None

    def sync_usage(self, provider, tokens, cost):
        """Registra el consumo en la tabla 'usage_logs'."""
        if not self.client: return False
        try:
            log_entry = {
                "provider": provider,
                "tokens": tokens,
                "cost_usd": cost,
                "timestamp": "now()"
            }
            self.client.table("usage_logs").insert(log_entry).execute()
            return True
        except Exception as e:
            print(f"☁️ Supabase Sync Error (Usage): {e}")
            return False

    def execute_sql(self, query):
        """Ejecuta SQL arbitrario vía RPC 'exec_sql'."""
        if not self.client: return False
        try:
            # Call the RPC function we created in automate_supabase.py
            self.client.rpc('exec_sql', {'query': query}).execute()
            print(f"☁️ SQL Executed via RPC: {query[:50]}...")
            return True
        except Exception as e:
            print(f"☁️ SQL RPC Error: {e}")
            return False

from brain.pain_nerve import PainNerve
from brain.healer import HealerAgent
from brain.agent_zero import AgentZeroStub
from brain.experience_manager import ExperienceManager, MissionArbiter

# --- ORCHESTRATOR (The Brain) ---
class AgentOrchestrator:
    def __init__(self, env_path):
        self.env_path = env_path
        self.agent_zero = AgentZeroStub()
        self.healer = HealerAgent()
        self.exp_manager = ExperienceManager() 
        self.mission_arbiter = MissionArbiter() # Integration Cap 7
        self.groq_key = None
        self.deepseek_key = None
        self.gemini_key = None
        
        self.gemini_key = None
        
        self.clients = {}
        self.status = {'groq': False, 'deepseek': False, 'gemini': False}
        
        self.status = {'groq': False, 'deepseek': False, 'gemini': False}
        
        self.usage_stats = {
            'tokens_total': 0,
            'cost_usd': 0.0,
            'providers': {
                'groq': {'tokens': 0, 'cost': 0.0},
                'deepseek': {'tokens': 0, 'cost': 0.0},
                'gemini': {'tokens': 0, 'cost': 0.0}
            }
        }
        
        self.state_path = os.path.join(os.path.dirname(env_path), "nexus_state.json")
        
        # 1. Load Config (Env Vars) FIRST
        self.reload_config()
        self.load_system_prompt()
        
        # 2. Init Supabase (Needs Env Vars)
        self.supabase = SupabaseManager() # Cap 2 Integration
        
        # 3. Load State & Sync Stats
        self.nexus_state = self.load_nexus_state()
        
        # Ensure Schema for Chapter 5
        self.nexus_state.setdefault("evolution_level", 1)
        self.nexus_state.setdefault("experience_points", 0)
        self.nexus_state.setdefault("personality_traits", {"efficiency": 0.5, "creativity": 0.5})
        self.nexus_state.setdefault("objective_history", [])
        self.nexus_state.setdefault("achievements", [])
        self.nexus_state.setdefault("title", "Iniciado Nexus")
        
        self.usage_stats = self.nexus_state.get('usage_stats', {
            'tokens_total': 0,
            'cost_usd': 0.0,
            'providers': {
                'groq': {'tokens': 0, 'cost': 0.0},
                'deepseek': {'tokens': 0, 'cost': 0.0},
                'gemini': {'tokens': 0, 'cost': 0.0}
            }
        })
        
        print("CEREBRO: Inicializado. Memoria y Costos activos.")

    def load_nexus_state(self):
        """Carga el estado de memoria de largo plazo (Cloud Sync)."""
        # 1. Intentar cargar de Supabase (Cloud)
        cloud_state = self.supabase.load_state()
        if cloud_state:
            print("☁️ NEXUS: Estado sincronizado desde la nube.")
            return cloud_state

        # 2. Fallback a Local
        if os.path.exists(self.state_path):
            try:
                import json
                with open(self.state_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"objectives": [], "personality": "neutral", "evolution_level": 1}
        return {"objectives": [], "personality": "neutral", "evolution_level": 1}

    def save_nexus_state(self):
        """Guarda el estado de memoria (Local + Cloud Sync)."""
        try:
            # A. Update stats in state before saving
            self.nexus_state['usage_stats'] = self.usage_stats
            
            # B. Guardado Local
            import json
            with open(self.state_path, 'w', encoding='utf-8') as f:
                json.dump(self.nexus_state, f, indent=4)
            
            # B. Sincronización Cloud (Cap 2)
            self.supabase.save_state(self.nexus_state)
            
        except Exception as e:
            print(f"Error guardando estado: {e}")

    def load_system_prompt(self):
        """Loads the Master Prompt from the specific text file."""
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "MASTER_PROMPT.txt")
        try:
            if os.path.exists(prompt_path):
                 with open(prompt_path, "r", encoding="utf-8") as f:
                     self.system_prompt = f.read()
                 print("✅ CEREBRO: Prompt Maestro Cargado.")
            else:
                 print("⚠️ CEREBRO: Prompt Maestro NO encontrado. Usando fallback.")
                 self.system_prompt = "Eres NEXUS MASTER GEN. Orquesta la creación de software."
        except Exception as e:
             print(f"❌ Error cargando prompt: {e}")
             self.system_prompt = "Eres NEXUS MASTER GEN."

    def reload_config(self):
        """Recarga configuración desde .env"""
        try:
            if os.path.exists(self.env_path):
                load_dotenv(self.env_path, override=True)
                
                # 1. GROQ
                self.groq_key = os.getenv("GROQ_API_KEY")
                if self.groq_key and SDK_MODELS['groq']:
                    try:
                        self.clients['groq'] = Groq(api_key=self.groq_key)
                        self.status['groq'] = True
                    except: pass

                # 2. DEEPSEEK (OpenAI Client)
                self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
                if self.deepseek_key and SDK_MODELS['openai']:
                    try:
                        self.clients['deepseek'] = OpenAI(
                            api_key=self.deepseek_key, 
                            base_url="https://api.deepseek.com"
                        )
                        self.status['deepseek'] = True
                    except: pass
                
                # 3. GEMINI
                self.gemini_key = os.getenv("GEMINI_API_KEY")
                if self.gemini_key and SDK_MODELS['genai']:
                    try:
                        genai.configure(api_key=self.gemini_key)
                        self.clients['gemini'] = True # Marker
                        self.status['gemini'] = True
                    except: pass

                print(f"CEREBRO ONLINE: {list(self.clients.keys())}")
                # Optional: Auto-verify on load (can be slow, maybe skip or do async)
                # self.verify_all_connections() 
            else:
                 print("CEREBRO OFFLINE: No .env found")
        except Exception as e:
            print(f"Error recargando cerebro: {e}")

    def verify_connection(self, provider):
        """Verifies a specific provider and updates status."""
        try:
            if provider not in self.clients:
                self.status[provider] = False
                return False

            if provider == 'groq' and SDK_MODELS['groq']:
                # Cheap call to list models or similar
                self.clients['groq'].models.list()
            elif provider == 'deepseek' and SDK_MODELS['openai']:
                # Simple chat completion test
                self.clients['deepseek'].chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": "ping"}],
                    max_tokens=1
                )
            elif provider == 'gemini' and SDK_MODELS['genai']:
                model = genai.GenerativeModel('gemini-pro')
                model.generate_content("ping")
            
            self.status[provider] = True
            return True
        except Exception as e:
            print(f"Verification failed for {provider}: {e}")
            self.status[provider] = False
            return False

    def verify_all_connections(self):
        """Verifies all configured providers."""
        results = {}
        for p in ['groq', 'deepseek', 'gemini']:
            sdk_key = 'genai' if p == 'gemini' else ('openai' if p == 'deepseek' else 'groq')
            if (self.clients.get(p) or (p == 'gemini' and self.gemini_key)) and SDK_MODELS.get(sdk_key):
                results[p] = self.verify_connection(p)
        return results

    def save_keys(self, config_dict):
        """Guarda claves en .env"""
        try:
            lines = []
            if os.path.exists(self.env_path):
                with open(self.env_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            
            # Map of config keys to env vars
            env_map = {
                'groq': 'GROQ_API_KEY',
                'deepseek': 'DEEPSEEK_API_KEY',
                'gemini': 'GEMINI_API_KEY',
                'supabase_url': 'SUPABASE_URL',
                'supabase_key': 'SUPABASE_KEY'
            }

            final_lines = []
            updated_keys = []
            
            # Update existing lines
            for line in lines:
                found = False
                for key, env_var in env_map.items():
                    if line.startswith(f"{env_var}="):
                        if config_dict.get(key):
                            final_lines.append(f"{env_var}='{config_dict[key]}'\n")
                            updated_keys.append(key)
                        else:
                            final_lines.append(line) # Keep old if no new value
                        found = True
                        break
                if not found:
                    final_lines.append(line)
            
            # Append new keys if not in file
            if lines and not lines[-1].endswith('\n'):
                final_lines.append('\n')
                
            for key, env_var in env_map.items():
                if config_dict.get(key) and key not in updated_keys:
                    # Check if we already processed it (case where it wasn't in file)
                    # We need to check if we updated it in the loop. 
                    # Simpler: Just reconstruct the file or use set_key from dotenv, 
                    # but simple append works for now.
                    is_present = any(l.startswith(f"{env_var}=") for l in final_lines)
                    if not is_present:
                         final_lines.append(f"{env_var}='{config_dict[key]}'\n")

            with open(self.env_path, 'w', encoding='utf-8') as f:
                f.writelines(final_lines)
            
            self.reload_config()
            return True
        except Exception as e:
            print(f"Error saving keys: {e}")
            return False

    def process_request(self, user_input):
        print(f"🧠 ORCHESTRATOR: Procesando '{user_input}'...")
        response_text = ""
        
        # 1. SPECIAL COMMANDS
        if "/status" in user_input.lower():
            response_text = f"🟢 SISTEMA OPERACIONAL\n- Motores Activos: {list(self.clients.keys())}"
        elif "/help" in user_input.lower():
            response_text = "🆘 COMANDOS:\n- `/status`: Estado de motores\n- `/evolve`: Resumen evolutivo\n- `/help`: Ayuda"
        elif "/evolve" in user_input.lower():
            summary = self.exp_manager.summarize_session(self.nexus_state)
            achievements = self.nexus_state.get("achievements", [])
            badges = " ".join([MissionArbiter.MISSIONS[m]["badge"] for m in achievements])
            response_text = f"🧠 **SÍNTESIS COGNITIVA EXPANSIÓN**:\n{summary}\n\n📊 **ESTADO NEXUS**:\n- Rango: **{self.nexus_state['title']}**\n- Nivel: {self.nexus_state['evolution_level']}\n- XP: {self.nexus_state['experience_points']}\n- Logros: {badges if badges else 'Ninguno'}\n- Rasgos: {self.nexus_state['personality_traits']}"
        
        # 2. GENERATION LOOP (If no command response yet)
        if not response_text:
            errors = []
            max_retries = 3
            current_input = user_input
            
            for attempt in range(max_retries):
                success_gen = False
                for provider in ['groq', 'deepseek', 'gemini']:
                    if self.status.get(provider, False):
                        try:
                            response_data = self._call_provider(provider, current_input)
                            response_text = response_data['content']
                            self._update_usage(provider, response_data.get('usage', {}))
                            success_gen = True
                            break 
                        except Exception as e:
                            errors.append(f"{provider}: {e}")
                
                # FALLBACK TO AGENT ZERO STUB (ESSENTIAL FOR OFFLINE/TEST)
                if not success_gen:
                    print("⚠️ Todos los proveedores fallaron. Usando AgentZeroStub.")
                    response_text = self.agent_zero.process(current_input)
                    success_gen = True 

                # SELF-HEALING (Simulated/Mechanical)
                if "test_break" in user_input:
                     cmd = [sys.executable, "-c", "import non_existent_package"]
                     _, _, pain_report = PainNerve.capture_exec(cmd)
                     diagnosis, treatment_msg = self.healer.diagnose(pain_report)
                     if diagnosis:
                         self.healer.heal(diagnosis)
                         response_text = f"🚑 Healer: {treatment_msg} \n✅ Sistema recuperado. Re-intentando..."
                         current_input = "He arreglado un error de importación. Continúa con mi pedido original."
                         continue
                
                break

        # 3. EVOLUTION & MISSIONS (Always execute)
        new_state_vars = self.exp_manager.process_interaction(self.nexus_state, user_input, response_text)
        self.nexus_state.update(new_state_vars)
        
        if new_state_vars.get("leveled_up"):
            response_text += f"\n\n✨ **NEXUS EVOLVED!** Nivel {self.nexus_state['evolution_level']}."
            
        new_missions = self.mission_arbiter.check_missions(self.nexus_state, user_input, response_text)
        for m_id in new_missions:
            mission = MissionArbiter.MISSIONS[m_id]
            self.nexus_state["experience_points"] += mission["xp_bonus"]
            response_text += f"\n\n🏆 **MISION COMPLETADA: {mission['name']}**\n{mission['badge']} {mission['desc']} (+{mission['xp_bonus']} XP)"

        # 4. TITLES & PERSISTENCE
        level = self.nexus_state["evolution_level"]
        titles = {1: "Iniciado", 5: "Explorador", 10: "Arquitecto", 20: "Maestro", 50: "Nexus-Ascendant"}
        for l_req, t_name in sorted(titles.items(), reverse=True):
            if level >= l_req:
                self.nexus_state["title"] = t_name
                break

        self.save_nexus_state()
        return response_text

    def _update_usage(self, provider, usage):
        """Actualiza estadísticas de consumo."""
        tokens = usage.get('total_tokens', 0)
        self.usage_stats['tokens_total'] += tokens
        self.usage_stats['providers'][provider]['tokens'] += tokens
        
        # Estimación simple de costos (Precios aproximados 2026)
        rates = {
            'groq': 0.70 / 1_000_000,     # Llama 3 70b
            'deepseek': 0.20 / 1_000_000, # DeepSeek V3
            'gemini': 0.50 / 1_000_000    # Gemini 1.5 Pro
        }
        
        cost = tokens * rates.get(provider, 0)
        self.usage_stats['cost_usd'] += cost
        self.usage_stats['providers'][provider]['cost'] += cost
        
        # Cloud Sync (Cap. 2)
        self.supabase.sync_usage(provider, tokens, cost)

    def _call_provider(self, provider, user_input):
        if provider == 'groq':
             completion = self.clients['groq'].chat.completions.create(
                messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": user_input}],
                model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=1024
            )
             return {
                 'content': completion.choices[0].message.content,
                 'usage': {
                     'total_tokens': completion.usage.total_tokens if hasattr(completion, 'usage') else 0
                 }
             }
        elif provider == 'deepseek':
             completion = self.clients['deepseek'].chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": user_input}],
                stream=False
            )
             return {
                 'content': completion.choices[0].message.content,
                 'usage': {
                     'total_tokens': completion.usage.total_tokens if hasattr(completion, 'usage') else 0
                 }
             }
        elif provider == 'gemini':
             try:
                model = genai.GenerativeModel('gemini-pro')
                # Gemini usage is a bit different
                response = model.generate_content(f"System: {self.system_prompt}\n\nUser: {user_input}")
                
                # Count tokens manually for better accuracy in Gemini if needed
                # For now use metadata if available
                tokens = model.count_tokens(user_input).total_tokens + model.count_tokens(response.text).total_tokens if response.text else 0
                
                if response and response.text:
                    return {
                        'content': response.text,
                        'usage': {'total_tokens': tokens}
                    }
                return {'content': "⚠️ Gemini devolvió una respuesta vacía.", 'usage': {}}
             except Exception as e:
                return {'content': f"⚠️ Gemini Error: {e}", 'usage': {}}
        return {'content': "Provider Error", 'usage': {}}

def main(page: ft.Page):
    print("DEBUG: Entered main")
    # SETUP LUXURY UI
    tokens = DesignRegistry.ARCHETYPES["aurora_glass"]
    page.title = "NEXUS MASTER GEN"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.expand = True
    page.padding = 0 # Full bleed for Aurora background
    
    # Global Aurora Gradient
    page.bgcolor = "black"
    main_bg = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=DesignRegistry.AURORA_GRADIENT_COLORS,
            stops=[0.0, 0.5, 1.0]
        ),
    )
    
    print("DEBUG: Page configured, adding background")
    # page.add(main_bg) # Wait, main_bg isn't added yet?
    # Ah, the original code didn't add main_bg here? Let's check below.
    # It seems main_bg is created but not added? Or added later?
    
    page.update()
    print("DEBUG: Page updated")
    
    # Responsive Logic (Chapter 3)
    def on_page_resize(e):
        cols = ResponsiveScanner.get_column_count(page.width)
        print(f"Resize: Width={page.width}, Cols={cols}")
        if factory_grid:
            factory_grid.runs_count = cols
            factory_grid.update()
    page.on_resize = on_page_resize
    
    NEON_CYAN = "#00f2ff"
    
    print("Sistema iniciado")
    
    # CHECK KNOWLEDGE BASE
    kb_path = os.path.join(os.getcwd(), "brain")
    if os.path.exists(kb_path):
        print(f"Knowledge Base Activa: {len(os.listdir(kb_path))} protocolos cargados.")
    else:
        print("Knowledge Base no encontrada.")
    
    # BACKEND
    agent = None
    factory = None
    try:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        env_path = os.path.join(data_dir, ".env")
        agent = AgentOrchestrator(env_path)
        factory = FactoryManager("Factory")
        print("Backend conectado")
    except Exception as e:
        print(f"Backend error: {e}")
    
    # === MÓDULO BRAIN ===
    brain_chat = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE, expand=True)
    
    def add_message(text, sender="user"):
        msg = ft.Container(
            content=ft.Text(text, color="white", font_family="Consolas"),
            bgcolor="#00334466" if sender == "user" else "#00000066", # Semi-transparent
            padding=15,
            border_radius=10,
            border=ft.border.all(1, NEON_CYAN if sender == "user" else "white10"),
            blur=5 # Add glass effect to individual messages
        )
        row = ft.Row([msg], alignment=ft.MainAxisAlignment.END if sender == "user" else ft.MainAxisAlignment.START)
        chat_list.controls.append(row)
        chat_list.update()
        page.update()
    
    def send_msg(e):
        # Using GlassInput: access inner field
        if not brain_input.input_field.value: return
        text = brain_input.input_field.value
        brain_input.input_field.value = ""
        add_message(text, "user")
        
        if agent:
            try:
                response = agent.process_request(text)
                add_message(response, "agent")
                # Update Matrix if visible or just update stats silently
                refresh_matrix_ui()
            except Exception as ex:
                add_message(f"Error: {ex}", "agent")
        else:
            add_message(f"⚠️ Backend no disponible ({SDK_MODELS})", "agent")
        
        brain_input.input_field.focus()
    
    # Shadowed definition removed

    
    # === MÓDULO BRAIN (Aurora Glass) ===
    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )
    
    brain_input = GlassInput(
        hint_text="Comando Nexus...",
        on_submit=send_msg,
        icon="terminal",
        expand=True
    )
    
    brain_module = DesignRegistry.get_glass_card(
        content=ft.Column([
            ft.Text("BRAIN - Core Intelligence", size=20, weight="bold", color=DesignRegistry.NEON_CYAN),
            ft.Divider(color=DesignRegistry.GLASS_BORDER),
            chat_list,
            ft.Container(height=10),
            ft.Row([
                brain_input,
                DesignRegistry.get_neon_button("ENVIAR", "send", on_click=send_msg)
            ])
        ]),
        visible=True,
        expand=True
    )
    
    # === MÓDULO FACTORY ===
    # === MÓDULO FACTORY ===
    
    # State for selected archetype
    selected_archetype = {"name": None}

    def update_archetype_selection(name):
        selected_archetype["name"] = name
        # Refresh visual state of cards
        for control in archetypes_grid.controls:
            # Each control is a Container -> Column -> (Icon, Text)
            # We need to update border of the outer container
            if isinstance(control, ft.Container):
                is_selected = control.data == name
                control.border = ft.border.all(2, NEON_CYAN if is_selected else "transparent")
                control.bgcolor = "#222222" if is_selected else "#1a1a1a"
        page.update()

    def build_architecture_card(name, content_control):
        return ft.Container(
            content=content_control,
            width=160,
            height=200, # Taller to fit content + labels
            border_radius=15,
            padding=0,
            data=name,
            on_click=lambda e: update_archetype_selection(name),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT_CUBIC),
            border=ft.border.all(2, "transparent"),
            bgcolor="#0a0a0a" # Base bg
        )

    # --- VISUAL STYLES GENERATORS ---

    def content_liquid_glass():
        """Optimized Liquid Glass for Desktop/Web Compatibility"""
        return ft.Container(
            # Stack removed to simplify rendering on desktop
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=["#00C6FF", "#0072FF"] # Vibrant Cyan to Blue
            ),
            width=160,
            height=200,
            border_radius=15,
            border=ft.border.all(1, "white54"),
            padding=15,
            alignment=ft.Alignment(0, 0),
            content=ft.Column([
                 ft.Icon("water_drop", color="white", size=40),
                 ft.Text("Liquid Glass", weight="bold", size=14, color="white"),
                 ft.Container(
                     bgcolor="white24", 
                     padding=5, 
                     border_radius=5,
                     content=ft.Text("Fluido. Brillante.", size=10, color="white", text_align="center")
                 )
            ], alignment="center", spacing=5)
        )

    def content_bento_grid():
        """Optimized Bento for High Contrast"""
        return ft.Container(
            bgcolor="#1a1a1a",
            border_radius=15,
            padding=10,
            border=ft.border.all(1, "#333333"),
            content=ft.Column([
                ft.Row([
                    ft.Container(bgcolor="#ff9900", height=40, expand=2, border_radius=5),
                    ft.Container(bgcolor="#444444", height=40, expand=1, border_radius=5),
                ], spacing=5),
                ft.Row([
                    ft.Container(bgcolor="#444444", height=40, expand=1, border_radius=5),
                    ft.Container(bgcolor="#2a2a2a", height=40, expand=2, border_radius=5, border=ft.border.all(1, "white24")),
                ], spacing=5),
                ft.Container(expand=True),
                ft.Text("Bento", weight="bold", size=14, color="white"),
                ft.Text("Modular. Organizado.", size=10, color="#888888")
            ], spacing=5, alignment="center")
        )

    def content_minimal():
        return ft.Container(
            bgcolor="black",
            border=ft.border.all(1, "white"),
            border_radius=15,
            padding=15,
            content=ft.Column([
                ft.Container(expand=True),
                ft.Text("Aa", size=40, weight="bold", color="white", font_family="Verdana"),
                ft.Container(height=1, bgcolor="white", width=40),
                ft.Container(expand=True),
                ft.Text("MINIMAL", weight="bold", size=12, color="white"),
                ft.Text("Esencialidad Pura", size=10, color="#white")
            ], alignment="center", horizontal_alignment="center", spacing=5)
        )

    archetypes_grid = ft.Row(
        controls=[
            build_architecture_card("Liquid Glass", content_liquid_glass()),
            build_architecture_card("Bento", content_bento_grid()),
            build_architecture_card("Minimal", content_minimal())
        ],
        wrap=True,
        spacing=20,
        run_spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # === MÓDULO FACTORY (Aurora Glass) ===
    factory_grid = ft.GridView(
        expand=False, # Changed to False to fit in ScrollColumn
        height=400,   # Fixed height for verify
        runs_count=3,
        max_extent=300,
        child_aspect_ratio=1.0,
        spacing=10,
        run_spacing=10,
    )
    
    factory_module = DesignRegistry.get_glass_card(
        content=ft.Column([
            ft.Text("FACTORY - Trinity Generator", size=20, weight="bold", color=DesignRegistry.NEON_CYAN),
            ft.Divider(color=DesignRegistry.GLASS_BORDER),
            
            ft.Text("Selecciona una Arquitectura", color="white", size=16),
            ft.Container(
                content=archetypes_grid,
                padding=20,
                border=ft.border.all(1, DesignRegistry.GLASS_BORDER),
                border_radius=10,
                bgcolor=DesignRegistry.GLASS_BG
            ),
            
            ft.Container(height=20),
            ft.TextField(hint_text="Nombre del proyecto", color="white", width=400, border_color=DesignRegistry.GLASS_BORDER, cursor_color=DesignRegistry.NEON_CYAN, text_style=ft.TextStyle(font_family="Roboto Mono")),
            ft.TextField(hint_text="Descripción", color="white", width=400, multiline=True, min_lines=3, border_color=DesignRegistry.GLASS_BORDER, cursor_color=DesignRegistry.NEON_CYAN, text_style=ft.TextStyle(font_family="Roboto Mono")),
            
            ft.Container(height=20),
            
            ft.Text("Proyectos Activos (Cloud DB)", size=16, color="white"),
            ft.Container(
                content=factory_grid,
                border=ft.border.all(1, "white10"),
                border_radius=10,
                padding=10,
                bgcolor="#00000050"
            ),
            
            DesignRegistry.get_neon_button("GENERAR PROYECTO", "engineering", lambda e: generate_project_handler(e))
        ], spacing=10, scroll=ft.ScrollMode.AUTO),
        visible=False,
        expand=True
    )
    
    def generate_project_handler(e):
        # Retrieve inputs from fixed positions in the Column
        # Structure: Text(0), Divider(1), Text(2), Container(Grid)(3), Container(Spacer)(4), TextField(Name)(5), TextField(Desc)(6)
        name_input = factory_module.content.controls[5]
        desc_input = factory_module.content.controls[6]
        
        proj_name = name_input.value
        archetype = selected_archetype["name"]
        
        if not proj_name:
            add_message("⚠️ Error: El nombre del proyecto es obligatorio", "agent")
            return
            
        if not archetype:
             add_message("⚠️ Error: Selecciona una arquitectura visual", "agent")
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
    matrix_logs = ft.Column(spacing=5, scroll=ft.ScrollMode.ADAPTIVE, expand=True)
    
    # Stats controls
    total_tokens_txt = ft.Text("0", size=24, weight="bold", color=NEON_CYAN)
    total_cost_usd_txt = ft.Text("$0.00", size=24, weight="bold", color="#00ff00")
    total_cost_mxn_txt = ft.Text("$0.00 MXN", size=16, color="#00ff00")
    evolution_txt = ft.Text("Nivel 1", size=18, weight="bold", color="white")

    def build_stat_card(title, control, icon="analytics"):
        return ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(icon, color=NEON_CYAN, size=16), ft.Text(title, size=12, color="white60")]),
                control
            ], spacing=5),
            bgcolor="#1a1a1a",
            padding=15,
            border_radius=10,
            border=ft.border.all(1, "white12"),
            width=200
        )

    stats_row = ft.Row([
        build_stat_card("Tokens Totales", total_tokens_txt, "generating_tokens"),
        build_stat_card("Inversión (USD)", total_cost_usd_txt, "monetization_on"),
        build_stat_card("Inversión (MXN)", total_cost_mxn_txt, "payments"),
        build_stat_card("Evolución IA", evolution_txt, "auto_awesome")
    ], spacing=20, wrap=True)

    def refresh_matrix_ui():
        if agent:
            total_tokens_txt.value = f"{agent.usage_stats['tokens_total']:,}"
            total_cost_usd_txt.value = f"${agent.usage_stats['cost_usd']:.4f}"
            
            # Conv (Cap. 1.1.3.1.1.1)
            mxn_rate = float(os.getenv("TIPO_CAMBIO_USD_MXN", 20.5))
            mxn_cost = agent.usage_stats['cost_usd'] * mxn_rate
            total_cost_mxn_txt.value = f"${mxn_cost:.2f} MXN"
            
            evolution_txt.value = f"Nivel {agent.nexus_state.get('evolution_level', 1)}"
            page.update()

    # === MÓDULO MATRIX (Aurora Glass) ===
    matrix_rows = ft.Column(scroll=ft.ScrollMode.AUTO)
    matrix_logs = ft.Column(scroll=ft.ScrollMode.AUTO)
    
    matrix_module = DesignRegistry.get_glass_card(
        content=ft.Column([
            ft.Text("MATRIX - Data & Logs", size=20, weight="bold", color=DesignRegistry.NEON_CYAN),
            ft.Divider(color=DesignRegistry.GLASS_BORDER),
            
            # KPI Row
            ft.Text("Métricas de Sesión", weight="bold", color="white"),
            matrix_rows,
            
            ft.Divider(color=DesignRegistry.GLASS_BORDER),
            
            ft.Text("Bitácora de Eventos", weight="bold", color="white"),
            ft.Container(
                content=matrix_logs,
                height=300,
                border=ft.border.all(1, "white10"),
                border_radius=8,
                padding=10
            ),
            
            ft.Divider(color="transparent"),
            DesignRegistry.get_neon_button("LIMPIAR LOGS", "delete", lambda e: matrix_logs.controls.clear() or page.update()),
            DesignRegistry.get_neon_button("VERIFICAR ESTADO", "refresh", lambda e: refresh_matrix_ui())
        ]),
        visible=False,
        expand=True
    )
    
    # === MÓDULO CONFIG ===
    
    # Text Fields References
    tf_groq = ft.TextField(label="GROQ_API_KEY", password=True, can_reveal_password=True, width=600)
    tf_deepseek = ft.TextField(label="DEEPSEEK_API_KEY", password=True, can_reveal_password=True, width=600)
    tf_gemini = ft.TextField(label="GEMINI_API_KEY", password=True, can_reveal_password=True, width=600)
    
    tf_sb_url = ft.TextField(label="SUPABASE_URL", width=600)
    tf_sb_key = ft.TextField(label="SUPABASE_KEY", password=True, can_reveal_password=True, width=600)

    def load_current_config():
        """Carga valores actuales a los campos"""
        if agent:
            if agent.groq_key: tf_groq.value = agent.groq_key
            if agent.deepseek_key: tf_deepseek.value = agent.deepseek_key
            if agent.gemini_key: tf_gemini.value = agent.gemini_key
            
            # Load manually for supabase as they might not be in agent variables explicitly yet
            # But we can read from environment loaded by user
            tf_sb_url.value = os.getenv("SUPABASE_URL", "")
            tf_sb_key.value = os.getenv("SUPABASE_KEY", "")
            page.update()

    def save_config_handler(e):
        if not agent:
             add_message("❌ Agente no inicializado", "agent")
             return
             
        config_data = {
            'groq': tf_groq.value,
            'deepseek': tf_deepseek.value,
            'gemini': tf_gemini.value,
            'supabase_url': tf_sb_url.value,
            'supabase_key': tf_sb_key.value
        }
        
        success = agent.save_keys(config_data)
        if success:
            add_message("✅ Configuración guardada y recargada.", "agent")
            page.snack_bar = ft.SnackBar(ft.Text("Configuración Guardada"))
            page.snack_bar.open = True
            page.update()
        else:
            add_message("❌ Error al guardar configuración.", "agent")

    
    def get_status_icon(provider):
        is_active = False
        if agent and agent.status.get(provider):
            is_active = True
        return ft.Icon("fiber_manual_record", color="green" if is_active else "red", size=15)

    def test_conn_handler(e, provider):
        if not agent: return
        add_message(f"Probando conexión : {provider}...", "agent")
        res = agent.verify_connection(provider)
        if res:
            add_message(f"✅ {provider}: CONECTADO", "agent")
        else:
            add_message(f"❌ {provider}: FALLÓ", "agent")
        
        # Update Icon
        # We need a way to reference the icon. 
        # Refetching logic simplifies state management here
        load_current_config()


    config_module = DesignRegistry.get_glass_card(
        content=ft.Column([
            ft.Text("CONFIG - Nexus Core", size=20, weight="bold", color=NEON_CYAN),
            ft.Divider(color="white24"),
            
            ft.Text("Multi-Provider AI Keys", color="white", size=16),
            
            # GROQ
            ft.Row([get_status_icon('groq'), ft.Text("Groq API Key:", color="white")]),
            ft.Row([tf_groq, DesignRegistry.get_neon_button("VERIFICAR", "network_check", on_click=lambda e: test_conn_handler(e, 'groq'))]),
            
            # DEEPSEEK
            ft.Row([get_status_icon('deepseek'), ft.Text("DeepSeek API Key:", color="white")]),
            ft.Row([tf_deepseek, DesignRegistry.get_neon_button("VERIFICAR", "network_check", on_click=lambda e: test_conn_handler(e, 'deepseek'))]),
 
            # GEMINI
            ft.Row([get_status_icon('gemini'), ft.Text("Gemini API Key:", color="white")]),
            ft.Row([tf_gemini, DesignRegistry.get_neon_button("VERIFICAR", "network_check", on_click=lambda e: test_conn_handler(e, 'gemini'))]),
            
            ft.Container(height=20),
            ft.Text("Nexus Sync (Supabase)", color="white", size=16),
            tf_sb_url,
            tf_sb_key,
            
            ft.Container(height=20),
            DesignRegistry.get_neon_button("GUARDAR CONFIGURACIÓN", "save", on_click=save_config_handler),
            DesignRegistry.get_neon_button("RECARGAR VALORES", "sync", on_click=lambda e: load_current_config())
        ], spacing=10, scroll=ft.ScrollMode.AUTO),
        visible=False,
        expand=True
    )
    
    # Load initial
    load_current_config()
    
    # --- Final Assembly with Aurora Background ---
    # Global Background Gradient
    page.gradient = DesignRegistry.get_main_background()
    page.padding = 0 # Full bleed for gradient
    
    # Navigation Buttons (Neon)
    brain_btn = DesignRegistry.get_neon_button("BRAIN", "smart_toy", lambda e: switch_module("brain"), selected=True)
    factory_btn = DesignRegistry.get_neon_button("FACTORY", "precision_manufacturing", lambda e: switch_module("factory"), selected=False)
    matrix_btn = DesignRegistry.get_neon_button("MATRIX", "analytics", lambda e: switch_module("matrix"), selected=False)
    config_btn = DesignRegistry.get_neon_button("CONFIG", "settings", lambda e: switch_module("config"), selected=False)

    active_tab = "brain"

    def switch_module(module_name):
        nonlocal active_tab
        active_tab = module_name
        
        brain_module.visible = (module_name == "brain")
        factory_module.visible = (module_name == "factory")
        matrix_module.visible = (module_name == "matrix")
        config_module.visible = (module_name == "config")
        
        # Update Nav State
        # We need to recreate the buttons or update their state. 
        # Since get_neon_button returns a new Container, recreating nav_bar contents is cleaner or we update props manually.
        # But we don't have references to the inner Container logic easily without a proper Component class.
        # For simplicity in this script, we'll brute-force update the styles of the existing objects if possible,
        # OR just re-render the navbar (less efficient). 
        # Actually, let's just manually update properties corresponding to the 'selected' logic in DesignRegistry.
        
        for btn, name in [(brain_btn, "brain"), (factory_btn, "factory"), (matrix_btn, "matrix"), (config_btn, "config")]:
             is_sel = (name == module_name)
             accent = DesignRegistry.NEON_CYAN
             btn.bgcolor = accent if is_sel else "#00000000"
             btn.border = ft.border.all(1, accent) if not is_sel else None
             content_row = btn.content
             for control in content_row.controls:
                 control.color = "black" if is_sel else accent
                 if isinstance(control, ft.Text):
                     control.weight = ft.FontWeight.BOLD if is_sel else ft.FontWeight.NORMAL
             btn.update()
        
        if module_name == "matrix":
            refresh_matrix_ui()
            
        page.update()

    # 1. Header (Floating Island)
    header = ft.Container(
        content=ft.Row([
            ft.Icon("auto_mode", color=DesignRegistry.NEON_CYAN, size=30),
            DesignRegistry.get_header_label("NEXUS MASTER GEN"),
            ft.Container(expand=True),
            ft.Icon("wifi", color="green", size=20),
            ft.Text("ONLINE", color="green", font_family="Roboto Mono")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=30, vertical=15),
        bgcolor="#0f172a66", # Semi-transparent dark
        blur=10,
        border_radius=ft.BorderRadius(0, 0, 20, 20), # Rounded bottom
        border=ft.border.only(bottom=ft.BorderSide(1, DesignRegistry.GLASS_BORDER))
    )
    
    # 2. Reference Nav Bar for Layout
    nav_bar = ft.Container(
        content=ft.ResponsiveRow([
            ft.Column([brain_btn], col={"xs": 6, "md": 3}),
            ft.Column([factory_btn], col={"xs": 6, "md": 3}),
            ft.Column([matrix_btn], col={"xs": 6, "md": 3}),
            ft.Column([config_btn], col={"xs": 6, "md": 3}),
        ]),
        padding=10
    )

    # 3. Main Content Area (Glass Panel)
    content_area = ft.Container(
        content=ft.Column([
            brain_module,
            factory_module,
            matrix_module,
            config_module
        ], expand=True),
        expand=True,
        padding=10
    )

    # Main Layout Stack (Aurora Background + Content)
    page.add(
        ft.Stack([
            main_bg, # Layer 0: Gradient
            ft.Column([ # Layer 1: UI
                header,
                nav_bar,
                content_area
            ], expand=True)
        ], expand=True)
    )
    
    page.update()
    
    # Mensaje inicial
    add_message("Nexus Master Gen (Aurora Edition) iniciado.", "agent")
    print("Interfaz Aurora lista")

if __name__ == "__main__":
    print("=== NEXUS MASTER GEN ===")
    try:
        if os.getenv("ATOLLI_WEB_MODE") == "true":
            print("Force launching in WEB MODE (CanvasKit Renderer)...")
            ft.app(target=main, view=ft.AppView.WEB_BROWSER, web_renderer="canvaskit")
        else:
            ft.app(target=main)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press ENTER...")
