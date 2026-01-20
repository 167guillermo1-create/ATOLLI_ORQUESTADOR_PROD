import math

class ExperienceManager:
    """
    Gestor de Evolución Cogitativa (Chapter 5).
    Calcula XP, niveles y rasgos de personalidad basados en la interacción.
    """
    
    XP_PER_LEVEL_BASE = 100
    XP_MULTIPLIER = 1.5

    @staticmethod
    def calculate_xp_gain(user_input, response_length):
        """
        Calcula cuánta experiencia se gana por una interacción.
        """
        # Base por complejidad del input
        base_xp = len(user_input.split()) * 2
        # Bonus por profundidad de respuesta (simulado)
        bonus_xp = min(50, response_length // 10)
        
        return base_xp + bonus_xp

    @staticmethod
    def get_xp_for_level(level):
        """Calcula el XP total necesario para alcanzar un nivel."""
        if level <= 1: return 0
        return int(ExperienceManager.XP_PER_LEVEL_BASE * (ExperienceManager.XP_MULTIPLIER ** (level - 2)))

    def process_interaction(self, current_state, user_input, response_text):
        """
        Procesa una interacción y retorna el estado actualizado.
        """
        # 1. Calcular Ganancia
        xp_gain = self.calculate_xp_gain(user_input, len(response_text))
        
        # 2. Actualizar XP
        new_xp = current_state.get("experience_points", 0) + xp_gain
        current_level = current_state.get("evolution_level", 1)
        
        # 3. Verificar Level Up
        next_level_xp = self.get_xp_for_level(current_level + 1)
        leveled_up = False
        
        if new_xp >= next_level_xp:
            current_level += 1
            leveled_up = True
            print(f"✨ NEXUS EVOLUTION: Level Up to {current_level}!")

        # 4. Actualizar Rasgos de Personalidad (Simple Keyword Analysis)
        traits = current_state.get("personality_traits", {"efficiency": 0.5, "creativity": 0.5})
        
        input_lower = user_input.lower()
        if any(word in input_lower for word in ["rápido", "fast", "corto", "resumen"]):
            traits["efficiency"] = min(1.0, traits["efficiency"] + 0.01)
        if any(word in input_lower for word in ["crea", "inventa", "estilo", "decoración"]):
            traits["creativity"] = min(1.0, traits["creativity"] + 0.01)

        # 5. Actualizar Historial de Objetivos (Nombres cortos)
        history = current_state.get("objective_history", [])
        if len(user_input) > 5:
            history.append(user_input[:30] + "...")
        if len(history) > 10:
            history.pop(0)

        # Retornar nuevos valores
        return {
            "evolution_level": current_level,
            "experience_points": new_xp,
            "personality_traits": traits,
            "objective_history": history,
            "leveled_up": leveled_up
        }

    def summarize_session(self, state):
        """
        Sintetiza lo aprendido en la sesión (Chapter 5).
        """
        history = state.get("objective_history", [])
        if not history:
            return "Sesión inactiva."
        
        # Simple synthesis: joined last 3 objectives
        last_3 = history[-3:]
        summary = f"Últimas metas: {' | '.join(last_3)}"
        
        # Actualizar personalidad basado en la intensidad
        # Si hay muchos objetivos, la 'eficiencia' sube
        if len(history) > 5:
            state["personality_traits"]["efficiency"] = min(1.0, state["personality_traits"]["efficiency"] + 0.05)
            
        return summary

class MissionArbiter:
    """
    Motor de Misiones (Chapter 7).
    Detecta logros específicos y otorga bonificaciones.
    """
    
    MISSIONS = {
        "ARCHITECT": {
            "name": "Gran Arquitecto",
            "desc": "Enviar un comando de más de 40 palabras.",
            "xp_bonus": 150,
            "badge": "📐"
        },
        "HEALER": {
            "name": "Médico de Almas",
            "desc": "Activar una rutina de auto-saneamiento exitosa.",
            "xp_bonus": 100,
            "badge": "🚑"
        },
        "CODER": {
            "name": "Héroe del Código",
            "desc": "Solicitar la creación de un nuevo archivo o script.",
            "xp_bonus": 80,
            "badge": "💾"
        },
        "EXPLORER": {
            "name": "Explorador Nexus",
            "desc": "Consultar el estado evolutivo 3 veces.",
            "xp_bonus": 50,
            "badge": "🕵️"
        }
    }

    def check_missions(self, state, user_input, response_text):
        """
        Verifica si se han completado misiones y retorna la lista de nuevas completadas.
        """
        completed_now = []
        achievements = state.setdefault("achievements", [])
        
        # 1. Mission: ARCHITECT
        if "ARCHITECT" not in achievements and len(user_input.split()) > 40:
            completed_now.append("ARCHITECT")
            
        # 2. Mission: CODER
        if "CODER" not in achievements:
            if any(word in user_input.lower() for word in ["crear archivo", "escribir script", "nuevo py"]):
                completed_now.append("CODER")

        # 3. Mission: HEALER
        if "HEALER" not in achievements and "🚑 Healer:" in response_text:
            completed_now.append("HEALER")

        # 4. Mission: EXPLORER
        if "EXPLORER" not in achievements:
            history = state.get("objective_history", [])
            evolve_count = sum(1 for h in history if "/evolve" in h.lower())
            if evolve_count >= 3:
                completed_now.append("EXPLORER")

        # Registrar logros
        for m_id in completed_now:
            achievements.append(m_id)
            
        return completed_now
