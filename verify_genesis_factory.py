
import os
import sys
import shutil

# Add brain directory
sys.path.append(os.path.join(os.getcwd(), 'brain'))

from factory_manager import FactoryManager

def test_factory():
    print("INICIANDO PROTOCOLO DE PRUEBA DE FABRICA...")
    
    target_name = "TestGenesis"
    factory_dir = os.path.join(os.getcwd(), "Factory")
    target_path = os.path.join(factory_dir, target_name)
    
    # Cleanup previous test
    if os.path.exists(target_path):
        print(f"🧹 Limpiando prueba anterior: {target_path}")
        shutil.rmtree(target_path)
        
    manager = FactoryManager(factory_dir)
    
    print(f"Generando ecosistema: {target_name}...")
    try:
        path, manifest_path = manager.create_ecosystem_scaffold(target_name)
        print(f"Generación reportada en: {path}")
    except Exception as e:
        print(f"❌ Error crítico en generación: {e}")
        return

    # VALIDATION PHASE
    print("\nVERIFICANDO BLINDAJE (SHIELDING)...")
    
    # 1. Requirements Check
    req_path = os.path.join(path, "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r") as f:
            content = f.read()
        
        if "flet==0.80.2" in content:
            print("requirements.txt: VALIDADO (flet==0.80.2)")
        else:
            print(f"requirements.txt: VULNERABLE.\nContenido:\n{content}")
    else:
        print("requirements.txt: NO ENCONTRADO")

    # 2. GitHub Workflow Check
    yml_path = os.path.join(path, ".github", "workflows", "nexus_trinity.yml")
    if os.path.exists(yml_path):
         with open(yml_path, "r") as f:
            content = f.read()
            
         if "pip install flet==0.80.2" in content:
             print("✅ CI/CD Workflow: VALIDADO (flet==0.80.2)")
         else:
             print("❌ CI/CD Workflow: VULNERABLE (Versión no fijada)")
    else:
        print("ℹ️ CI/CD Workflow: No generado (Esto puede ser normal si NexusSeed no tenía .github)")

    # 3. Structure Check
    main_path = os.path.join(path, "web_portal", "main.py")
    if os.path.exists(main_path):
        print("Estructura Base: CORRECTA (web_portal/main.py existe)")
    else:
        print("Estructura Base: INUSUAL (No se halló web_portal/main.py)")

    print("\nPRUEBA DE FABRICA COMPLETADA.")

if __name__ == "__main__":
    test_factory()
