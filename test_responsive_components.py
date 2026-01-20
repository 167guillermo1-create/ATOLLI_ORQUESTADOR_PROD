import sys
import os
import unittest
# Mock Flet
from unittest.mock import MagicMock

# Add path
sys.path.append(os.getcwd())

# We need to ensure flet imports work even if we mock some things
import flet as ft
from brain.design_system import ResponsiveScanner, DesignRegistry
from brain.ui_components import LuxuryStepper, GlassInput, SmartTooltip

class TestChapter3UI(unittest.TestCase):
    
    def test_responsive_scanner(self):
        """Verify device detection logic."""
        print("\nTesting ResponsiveScanner...")
        self.assertEqual(ResponsiveScanner.get_device_type(400), "MOBILE")
        self.assertEqual(ResponsiveScanner.get_device_type(800), "TABLET")
        self.assertEqual(ResponsiveScanner.get_device_type(1920), "DESKTOP")
        
        self.assertEqual(ResponsiveScanner.get_column_count(400), 1)
        self.assertEqual(ResponsiveScanner.get_column_count(800), 2)
        self.assertEqual(ResponsiveScanner.get_column_count(1200), 4)
        print("   [OK] Responsive Logic Verified")

    def test_components_instantiation(self):
        """Verify new components instantiate without syntax errors."""
        print("\nTesting Component Instantiation...")
        
        # Stepper
        stepper = LuxuryStepper(current_step=1, total_steps=3)
        self.assertIsNotNone(stepper)
        print("   [OK] LuxuryStepper created")
        
        # GlassInput
        inp = GlassInput(hint_text="Test", icon="search")
        self.assertIsNotNone(inp)
        print("   [OK] GlassInput created")
        
        # Tooltip
        tooltip = SmartTooltip(message="AI Help")
        self.assertIsNotNone(tooltip)
        print("   [OK] SmartTooltip created")

if __name__ == "__main__":
    unittest.main()
