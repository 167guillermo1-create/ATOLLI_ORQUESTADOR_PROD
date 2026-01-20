import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add main path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import AgentOrchestrator
from brain.pain_nerve import PainNerve
from brain.healer import HealerAgent

class TestSelfHealing(unittest.TestCase):
    def setUp(self):
        # Env path is required by constructor
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", ".env")
        self.orchestrator = AgentOrchestrator(env_path=env_path)
        
    def test_infection_response(self):
        print("\n🦠 INJECTING VIRUS: 'test_break' payload...")
        
        # Trigger the logic we added to main.py
        # It's mocked to run a subprocess that fails with ImportError
        # We want to verified that it returns a "System recovered" message
        
        # Note: In a real environment, we don't want to actually install junk packages.
        # But 'non_existent_package' will fail to install too, so the Healer will fail the CURE but PASS the diagnosis.
        # We mock the Healer's install method to pass.
        
        with patch.object(HealerAgent, 'heal', return_value="Simulated Cure Applied") as mock_heal:
             response = self.orchestrator.process_request("test_break")
             
             print(f"🛡️ IMMUNE RESPONSE: {response}")
             
             # Assertions
             self.assertIn("Error detectado", response)
             self.assertIn("Healer:", response)
             self.assertIn("Sistema recuperado", response)
             
             # Verify Heal was called
             mock_heal.assert_called_once()
             print("✅ Antibodies Deployed: Healer.heal() was triggered.")

if __name__ == "__main__":
    unittest.main()
