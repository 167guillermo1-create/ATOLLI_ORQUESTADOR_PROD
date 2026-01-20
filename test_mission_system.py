import unittest
import os
import sys
from unittest.mock import MagicMock, patch

# Add main path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import AgentOrchestrator
from brain.experience_manager import MissionArbiter

class TestMissionSystem(unittest.TestCase):
    def setUp(self):
        self.env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", ".env")
        with patch('main.SupabaseManager') as mock_sb:
            mock_sb.return_value.load_state.return_value = None
            mock_sb.return_value.save_state.return_value = True
            self.orchestrator = AgentOrchestrator(env_path=self.env_path)
            self.orchestrator.nexus_state = {
                "evolution_level": 1,
                "experience_points": 0,
                "personality_traits": {"efficiency": 0.5, "creativity": 0.5},
                "objective_history": [],
                "achievements": [],
                "title": "Iniciado"
            }

    def test_architect_mission(self):
        print("\n📐 TESTING MISSION: ARCHITECT (Complexity)...")
        # Very long prompt
        long_prompt = "Este es un comando extremadamente largo diseñado para probar la capacidad de arquitectura de Nexus. " * 5 
        response = self.orchestrator.process_request(long_prompt)
        
        self.assertIn("ARCHITECT", self.orchestrator.nexus_state["achievements"])
        self.assertIn("MISION COMPLETADA: Gran Arquitecto", response)
        print(f"✅ ARCHITECT Mission Passed. XP={self.orchestrator.nexus_state['experience_points']}")

    def test_coder_mission(self):
        print("\n💾 TESTING MISSION: CODER (Keywords)...")
        coder_prompt = "Necesito crear archivo python para procesar datos."
        response = self.orchestrator.process_request(coder_prompt)
        
        self.assertIn("CODER", self.orchestrator.nexus_state["achievements"])
        self.assertIn("Héroe del Código", response)
        print(f"✅ CODER Mission Passed. XP={self.orchestrator.nexus_state['experience_points']}")

    def test_evolution_titles(self):
        print("\n🎖️ TESTING TITLES: Progression check...")
        # Force level up to Level 5 (Explorador)
        self.orchestrator.nexus_state["evolution_level"] = 5
        self.orchestrator.process_request("ping")
        
        self.assertEqual(self.orchestrator.nexus_state["title"], "Explorador")
        print(f"✅ Title Progression Passed: {self.orchestrator.nexus_state['title']}")

if __name__ == "__main__":
    unittest.main()
