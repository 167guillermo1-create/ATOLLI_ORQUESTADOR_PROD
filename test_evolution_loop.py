import unittest
import os
import sys
from unittest.mock import MagicMock, patch

# Add main path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import AgentOrchestrator
from brain.experience_manager import ExperienceManager

class TestEvolutionLoop(unittest.TestCase):
    def setUp(self):
        # Env path for orchestrator
        self.env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", ".env")
        # Mock Supabase to avoid cloud hits
        with patch('main.SupabaseManager') as mock_sb:
            mock_sb.return_value.load_state.return_value = None
            mock_sb.return_value.save_state.return_value = True
            self.orchestrator = AgentOrchestrator(env_path=self.env_path)
            # Ensure nexus_state is a real dict
            self.orchestrator.nexus_state = {
                "evolution_level": 1,
                "experience_points": 0,
                "personality_traits": {"efficiency": 0.5, "creativity": 0.5},
                "objective_history": []
            }

    def test_xp_and_level_up(self):
        print("\n📈 TESTING EVOLUTION: Simulating high-complexity interactions...")
        
        # Initial state
        self.orchestrator.nexus_state["experience_points"] = 0
        self.orchestrator.nexus_state["evolution_level"] = 1
        
        # Simulate interaction
        # We need a long input/response to trigger XP gain fast in the stub
        complex_prompt = "Crear un sistema de orquestación masivo con decoradores premium y Aurora Glass UI"
        
        # We simulate 10 interactions to ensure level up (Target level 2 is 100 XP)
        for i in range(10):
            response = self.orchestrator.process_request(complex_prompt)
            print(f"   Iteration {i+1}: XP={self.orchestrator.nexus_state['experience_points']}")

        # Assertions
        final_level = self.orchestrator.nexus_state["evolution_level"]
        print(f"🏁 FINAL LEVEL: {final_level}")
        
        self.assertGreater(final_level, 1, "Nexus should have leveled up after 10 complex interactions")
        self.assertGreater(self.orchestrator.nexus_state["experience_points"], 100)
        self.assertTrue(len(self.orchestrator.nexus_state["objective_history"]) > 0)
        
        print("✅ Evolution Loop Verified: XP Gain -> Level Up -> Persistent History.")

if __name__ == "__main__":
    unittest.main()
