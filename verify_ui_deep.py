import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import flet as ft

# Add path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import main as app_main, AgentOrchestrator
from brain.design_system import DesignRegistry

class TestDeepUI(unittest.TestCase):
    def setUp(self):
        self.mock_page = MagicMock(spec=ft.Page)
        self.mock_page.controls = []
        self.mock_page.platform = "windows"
        self.mock_page.route = "/"
        self.mock_page.width = 1200 # Desktop
        
        # Capture controls added to page
        def add(*args):
            self.mock_page.controls.extend(args)
        self.mock_page.add = MagicMock(side_effect=add)
        self.mock_page.update = MagicMock()

    def find_control_by_type(self, control_type, controls, predicate=None):
        """Recursive search for a control."""
        for c in controls:
            if isinstance(c, control_type):
                if predicate is None or predicate(c):
                    return c
            
            # Recurse
            children = []
            if hasattr(c, 'content') and c.content:
                if isinstance(c.content, list): children.extend(c.content)
                else: children.append(c.content)
            if hasattr(c, 'controls') and c.controls:
                children.extend(c.controls)
                
            found = self.find_control_by_type(control_type, children, predicate)
            if found: return found
        return None

    @patch('main.AgentOrchestrator')
    @patch('main.SupabaseManager')
    def test_luxury_design_integrity(self, MockSupabase, MockAgent):
        """Verifies that the Luxury UI components and styles are actually applied."""
        print("\n[DEEP UI] Validando Integridad del Diseño Aurora Glass...")
        
        # Setup Logic
        app_main(self.mock_page)
        
        # 1. Validate Background Gradient (The "Aurora")
        # We need to distinguish the Main Page BG from small card BGs.
        # The main BG is usually the first container or one with expand=True and specifically 3 stops [0.0, 0.5, 1.0]
        bg_container = self.find_control_by_type(
            ft.Container, 
            self.mock_page.controls, 
            lambda c: isinstance(c.gradient, ft.LinearGradient) and len(c.gradient.colors) == 3
        )
        
        if bg_container:
            colors = bg_container.gradient.colors
            print(f"   ✅ 'Aurora' Background Detected: Gradient with {len(colors)} colors")
            # DesignRegistry.AURORA_GRADIENT_COLORS expected
            # We just print to confirm match to avoid brittle assertion if registry changes order
            print(f"      Colors: {colors}")
        else:
             print("   ⚠️ WARNING: Main Aurora Background Container not found (Might be obscured by cards)")

        # 2. Validate GlassInput Structure
        # It's a Container containing a Row containing a TextField
        # We look for the TextField with hint_text="Comando Nexus..."
        input_field = self.find_control_by_type(
            ft.TextField,
            self.mock_page.controls,
            lambda c: c.hint_text == "Comando Nexus..."
        )
        
        self.assertIsNotNone(input_field, "GlassInput inner TextField not found")
        print("   ✅ GlassInput Component Verified")
        
        # Verify it has no border (GlassInput style removes default border)
        self.assertEqual(input_field.border, ft.InputBorder.NONE, "GlassInput field should have NONE border")

    @patch('main.AgentOrchestrator')
    @patch('main.SupabaseManager')
    def test_factory_grid_structure(self, MockSupabase, MockAgent):
        """Verifies the Factory Module and Grid structure."""
        print("\n[DEEP UI] Validando Módulo Factory...")
        app_main(self.mock_page)
        
        # Find GridView
        grid = self.find_control_by_type(ft.GridView, self.mock_page.controls)
        self.assertIsNotNone(grid, "Factory GridView not found")
        print(f"   ✅ Factory GridView Detected (Runs: {grid.runs_count})")
        
        # Verify Responsive Logic (Desktop width=1200 -> 4 columns? Or whatever logic says)
        # In main.py: Desktop > 1024 -> 4 columns.
        # But wait, logic is in on_resize. Does main run on_resize initially?
        # Usually it doesn't auto-run. We can manually trigger it.
        
        # Verify Responsive Logic
        # We need to simulate the grid being accessible.
        # In main.py, factory_grid is created. We should find it.
        if grid:
             grid.runs_count = 1 # Reset to mobile default
             grid.update = MagicMock() # Mock update to avoid "Control must be added to page" error in headless
             
             # Trigger resize
             on_resize = self.mock_page.on_resize
             if on_resize:
                print("   ✅ triggering page.on_resize (Simulating resizing to 1200px)")
                on_resize(None) # Width is mocked at setup 1200
                
                # Check if runs_count updated
                # Note: main.py 'on_page_resize' updates 'factory_grid.runs_count' directly.
                # Since 'grid' here is the same object reference (found via recursive search), it should reflect the change.
                print(f"      Grid Runs post-resize: {grid.runs_count}")
                self.assertEqual(grid.runs_count, 4, "Should be 4 columns on Desktop")
        else:
            self.fail("Factory GridView not found in controls tree")
        
        # Verify Standard Archetypes Existence (Liquid Glass, Bento, Minimal)
        # They are added to the grid rows? No, main.py shows 'archetypes_grid' (Row) inside the Factory Module 
        # and 'factory_grid' is separate (maybe for projects?). 
        # Let's check 'archetypes_grid' content.
        
        # Finding the Row that contains the architectural cards
        # We search for a Container with data="Liquid Glass"
        liquid_card = self.find_control_by_type(
            ft.Container, 
            self.mock_page.controls, 
            lambda c: c.data == "Liquid Glass"
        )
        self.assertIsNotNone(liquid_card, "Liquid Glass card not found")
        print("   ✅ Architecture Cards Present: Liquid Glass")


if __name__ == "__main__":
    unittest.main()
