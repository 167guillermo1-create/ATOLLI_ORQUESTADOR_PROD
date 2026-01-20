import os
import sys
import shutil
import io

# Force UTF-8 for Windows Console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Sync paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from brain.factory_manager import FactoryManager

def run_final_delivery():
    print("--- INICIANDO GENERACION DE SHOWCASE DE PRODUCCION ---")
    
    fm = FactoryManager("Factory")
    project_name = "Nexus_Production_Showcase"
    project_path = os.path.join(os.getcwd(), "Factory", project_name)
    
    # 1. Clean and Build
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
    
    print(f"[*] Construyendo Scaffolding para {project_name}...")
    fm.create_ecosystem_scaffold(project_name)
    
    shared_path = os.path.join(project_path, "shared")
    print("[*] Inyectando SyncCore y Tokens Premium...")
    fm.inject_sync_core(shared_path)
    # Using 'aurora_glass' which is the standard Premium archetype
    fm.inject_design_tokens(shared_path, archetype="aurora_glass")
    
    # 2. Add build wrappers inside the project
    print("[*] Agregando wrappers de distribucion...")
    
    win_build_content = """@echo off
echo [*] Iniciando Compilacion para Windows (EXE)...
cd ../..
python build_production.py
pause
"""
    with open(os.path.join(project_path, "build_windows.bat"), "w") as f:
        f.write(win_build_content)
        
    readme_content = f"""# {project_name} - Trinity Delivery
Este proyecto ha sido generado automaticamente por Nexus Master Gen en el Bucle Final de Auditoria.

## Entregables Multiplataforma

### 1. Windows (EXE)
- Use el script `build_windows.bat` en esta carpeta.
- Requiere Flet instalado (`pip install flet`).
- El binario se generara en `dist/`.

### 2. Android (APK)
- El workflow esta configurado en `.github/workflows/build_apk.yml`.
- Al hacer push a GitHub, se generara el APK automaticamente en Actions.

### 3. Web
- Ejecute `flet run --web main.py` en el orquestador principal.
- Use `--port 8590` para ver la versión de auditoría.

---
**NEXUS MASTER GEN - PRODUCTION READY**
"""
    with open(os.path.join(project_path, "DELIVERY_REPORT.md"), "w") as f:
        f.write(readme_content)

    print(f"[OK] SHOWCASE COMPLETADO: {project_path}")
    return True

if __name__ == "__main__":
    run_final_delivery()
