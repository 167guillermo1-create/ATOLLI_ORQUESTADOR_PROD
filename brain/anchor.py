import ast
import platform

class RealityAnchor:
    """
    El Ancla (The Anchor):
    Garantiza que el Agente y el Usuario no 'alucinen' con capacidades que no tienen.
    """
    
    FORBIDDEN_KEYWORDS = [
        "docker", "kubernetes", "tensorflow", "pytorch", "selenium", 
        "hackear", "crackear", "bitcoin mining"
    ]
    
    ALLOWED_IMPORTS = [
        "flet", "os", "sys", "json", "math", "datetime", "requests", "langchain",
        "chromadb", "random", "time", "threading", "subprocess", "re", "ast"
    ]

    def check_feasibility(self, user_request: str) -> dict:
        """
        Filtro B: El Guardián del Alcance (Scope Warden).
        Retorna {'valid': bool, 'reason': str}
        """
        request_lower = user_request.lower()
        
        # 1. Check for Impossible concepts
        for keyword in self.FORBIDDEN_KEYWORDS:
            if keyword in request_lower:
                return {
                    "valid": False, 
                    "reason": f"⚓ ANCLA ACTIVADA: El término '{keyword}' viola los protocolos de seguridad o capacidad portable."
                }
        
        # 2. Check for Hardware dependency
        if "gpu" in request_lower or "cuda" in request_lower:
             return {
                "valid": False, 
                "reason": "⚓ ANCLA ACTIVADA: Este sistema corre en CPU (Portable). No podemos usar aceleración GPU."
            }
            
        return {"valid": True, "reason": "Solicitud Viable."}

    def validate_generated_code(self, code: str) -> dict:
        """
        Filtro A: El Crítico de Código (Code Critic).
        Analiza el código Python antes de ejecutarlo.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"valid": False, "reason": f"Error de Sintaxis Python: {e}"}

        return {"valid": True, "reason": "Código Seguro."}

class NexusHealer:
    """
    SISTEMA DE ANTICUERPOS NEXUS (Dinámico):
    Carga el 'Firmware' mecánico para sanar el código sin requerir creatividad de la IA.
    """
    @staticmethod
    def heal_code(code: str) -> str:
        import re
        import json
        import os
        
        firmware_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "nexus_firmware.json")
        
        if not os.path.exists(firmware_path):
            return code # Fallback si no hay firmware

        try:
            with open(firmware_path, "r") as f:
                fw = json.load(f)
            rules = fw.get("mechanical_rules", {})
            
            # 1. Aplicar Reemplazos Directos (Animations, Borders, Radii, Tabs)
            for category in ["animations", "borders", "radii", "tabs"]:
                for rule in rules.get(category, []):
                    code = re.sub(rule["old"], rule["new"], code)
            
            # 2. Aplicar Mapa de Alineación
            align_rules = rules.get("alignments", {})
            for old, new in align_rules.items():
                code = re.sub(old, new, code)
            
            # 3. Aplicar Patrón de Iconos
            icon_cfg = rules.get("icons", {})
            if "pattern" in icon_cfg:
                def icon_fixer(match):
                    return icon_cfg["replacement"] % match.group(1).lower()
                code = re.sub(icon_cfg["pattern"], icon_fixer, code)
                
        except Exception as e:
            print(f"⚠️ Error en NexusHealer (Firmware): {e}")
            
        return code
