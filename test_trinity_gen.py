import os
import shutil
import json
import sys

# Agregar path del brain para poder importar módulos
sys.path.append(os.path.join(os.getcwd(), "brain"))

from factory_manager import FactoryManager

def test_trinity_gen():
    print("🧪 INICIANDO TEST: Trinity Generation Protocol")
    
    # 1. Setup
    factory = FactoryManager()
    test_proj_name = "TestTrinityGen"
    test_proj_path = os.path.join(os.getcwd(), "Factory", test_proj_name)
    
    # Clean previous run
    if os.path.exists(test_proj_path):
        print(f"🧹 Limpiando test anterior: {test_proj_path}")
        shutil.rmtree(test_proj_path)
        
    # 2. Execution
    print(f"⚙️ Invocando FactoryManager para '{test_proj_name}'...")
    try:
        path, dirs = factory.create_ecosystem_scaffold(test_proj_name)
        print(f"✅ Proyecto generado en: {path}")
    except Exception as e:
        print(f"❌ Error fatal en generación: {e}")
        return False
        
    # 3. Verification
    print("🔍 Auditando resultados...")
    
    # Check 1: SyncCore Existence (Proof of Clone)
    sync_core_path = os.path.join(path, "shared", "sync_core.py")
    if os.path.exists(sync_core_path):
        print("✅ SyncCore detectado (Clonado exitoso)")
    else:
        print("❌ SyncCore NO encontrado (Fallo de clonado)")
        return False
        
    # Check 2: Manifest Integrity
    manifest_path = os.path.join(path, "nexus_manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            data = json.load(f)
            
        if data["name"] == test_proj_name:
            print(f"✅ Manifiesto actualizado: name='{test_proj_name}'")
        else:
            print(f"❌ Manifiesto incorrecto: name='{data.get('name')}'")
            return False
            
        if "parent_seed" in data and data["parent_seed"] == "NexusSeed":
            print("✅ Linaje confirmado: parent_seed='NexusSeed'")
        else:
            print("❌ Linaje perdido en manifiesto")
            return False
    else:
        print("❌ Manifiesto no encontrado")
        return False
        
    print("\n🎉 TEST TRINITY: PASSED")
    return True

if __name__ == "__main__":
    test_trinity_gen()
