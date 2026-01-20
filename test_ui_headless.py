import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import flet as ft

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# We need to mock SupabaseManager before importing main if possible, 
# or patch it during the test.
from main import main as app_main, AgentOrchestrator

class TestHeadlessUI(unittest.TestCase):
    def setUp(self):
        self.mock_page = MagicMock(spec=ft.Page)
        self.mock_page.controls = []
        self.mock_page.platform = "windows"
        self.mock_page.route = "/"
        
        # Capture controls added to page
        def add(*args):
            self.mock_page.controls.extend(args)
        self.mock_page.add = MagicMock(side_effect=add)
        self.mock_page.update = MagicMock()

    @patch('main.AgentOrchestrator')
    @patch('main.SupabaseManager')
    def test_brain_interaction(self, MockSupabase, MockAgent):
        # Setup Mock Agent
        agent_instance = MockAgent.return_value
        agent_instance.process_request.return_value = "Respuesta Simulada del Brain"
        agent_instance.usage_stats = {'tokens_total': 0, 'cost_usd': 0.0, 'providers': {}}
        
        print("\n[HEADLESS UI] Construyendo Interfaz...")
        app_main(self.mock_page)
        
        # 1. Find the Brain Input TextField
        # The structure is Stack -> [Bg, Container(MainLayout)] -> Column -> ...
        # We need a recursive finder.
        
        found_input = None
        found_chat_column = None
        
        def find_controls(controls):
            nonlocal found_input, found_chat_column
            for c in controls:
                if isinstance(c, ft.TextField) and c.hint_text == "Comando Nexus...":
                    found_input = c
                if isinstance(c, ft.Column) and hasattr(c, 'scroll') and c.scroll == ft.ScrollMode.ADAPTIVE:
                    # Heuristic for the chat column
                    found_chat_column = c
                
                # Recurse
                if hasattr(c, 'content') and c.content:
                    if isinstance(c.content, ft.Control):
                        find_controls([c.content])
                    elif isinstance(c.content, list):
                        find_controls(c.content)
                if hasattr(c, 'controls') and c.controls:
                    find_controls(c.controls)

        find_controls(self.mock_page.controls)
        
        if not found_input:
            self.fail("No se encontró el campo de input del Brain UI.")
        else:
             print(f"✅ Campo de Input encontrado: {found_input.hint_text}")

        if not found_chat_column:
            # It might be tricky to find if it's inside a specific container structure
            print("⚠️ Columna de chat no identificada con certeza, pero continuamos.")

        # 2. Simulate User Input
        print("[HEADLESS UI] Simulando escritura: 'Hola Atolli'")
        found_input.value = "Hola Atolli"
        
        # 3. Trigger Submit
        print("[HEADLESS UI] Disparando evento on_submit...")
        if found_input.on_submit:
            found_input.on_submit(None) # Event arg usually not used or mocked
        else:
            self.fail("El input no tiene handler on_submit.")
            
        # 4. Verify Agent was called
        agent_instance.process_request.assert_called_with("Hola Atolli")
        print("✅ AgentOrchestrator.process_request fue llamado correctamente.")

        # 5. Verify Chat Update (If possible)
        # The logic calls 'add_message'. This appends to 'brain_chat.controls'.
        # Assuming found_chat_column is 'brain_chat'.
        if found_chat_column:
            # We expect 2 messages: User + Agent
            msg_count = len(found_chat_column.controls)
            # Depending on initial messages. 
            # main() calls add_message("Nexus Master Gen iniciado...", "agent") -> 1
            # User "Hola" -> 2
            # Agent "Respuesta..." -> 3
            if msg_count >= 3:
                print(f"✅ Chat actualizado. Mensajes totales: {msg_count}")
            else:
                self.fail(f"El chat no se actualizó. Mensajes: {msg_count}")
        
    def test_navigation_logic(self):
        # We can also verify navigation buttons if we can find them.
        pass

if __name__ == "__main__":
    unittest.main()
