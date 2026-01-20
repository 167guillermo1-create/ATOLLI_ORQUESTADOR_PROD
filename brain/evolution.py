import subprocess
import sys
import os

class EvolutionManager:
    """
    El Evolucionador:
    Permite que el Agente instale nuevas habilidades (librerías) en tiempo real.
    """
    
    def __init__(self, anchor):
        self.anchor = anchor

    def install_package(self, package_name: str) -> str:
        """
        Intenta instalar un paquete PIP en el entorno portable actual.
        """
        # 1. Check Reality Anchor
        if package_name in self.anchor.FORBIDDEN_KEYWORDS:
             return f"⚓ Evolution DENEGADA: El paquete '{package_name}' está prohibido por el Ancla."

        print(f"🧬 EVOLUCIÓN INICIADA: Instalando '{package_name}'...")
        
        try:
            # Use the current python executable to install into user site or venv
            # In a portable setup we might target a specific lib folder
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            return f"✅ EVOLUCIÓN COMPLETADA: '{package_name}' instalado. Soy más fuerte."
        except subprocess.CalledProcessError as e:
            return f"❌ EVOLUCIÓN FALLIDA: No pude instalar '{package_name}'. Error: {e}"

    def check_installed(self, package_name: str) -> bool:
        try:
            __import__(package_name)
            return True
        except ImportError:
            return False
