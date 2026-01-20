import subprocess
import os
import sys
import shutil

# Reconfigurar encoding al inicio
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def build():
    print("INICIANDO PROCESO DE COMPILACION PRODUCTION (NEXUS)")
    
    # 1. Definir Rutas
    project_root = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(project_root, "assets")
    dist_dir = os.path.join(project_root, "dist")
    
    if not os.path.exists(assets_dir):
        print("Error: Carpeta 'assets' no encontrada.")
        return

    print("   Compilando para Windows Executable...")
    try:
        # El comando 'flet build windows' es el estándar
        # Usamos --product "Nexus Master Gen" para el nombre del binario
        cmd = [
            "flet", "build", "windows",
            "--product", "Nexus Master Gen",
            "--description", "AI Orchestrator by Atolli",
            "--copyright", "Copyright 2026 Atolli",
            "--no-rich-output",
            "--yes"
        ]
        
        # Custom environment to force UTF-8 and avoid rich rendering issues
        build_env = os.environ.copy()
        build_env["PYTHONIOENCODING"] = "utf-8"
        build_env["PYTHONUTF8"] = "1"
        build_env["FLET_NO_RICH_OUTPUT"] = "1"
        
        result = subprocess.run(
            cmd, 
            cwd=project_root, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            env=build_env
        )
        
        if result.returncode == 0:
            print("COMPILACION EXITOSA")
            print(f"   Artefacto generado en: {os.path.join(dist_dir, 'windows')}")
        else:
            print("FALLO EN COMPILACION")
            print(f"   Error: {result.stderr}")
            print(f"   Output: {result.stdout}")

    except FileNotFoundError:
        print("Error: Flet CLI no encontrado. ¿Has corrido 'pip install flet'? ")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    build()
