import subprocess
import sys
import time
import os

# Windows Console Encoding Fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Import Brain
sys.path.append(os.path.join(os.path.dirname(__file__), "brain"))
try:
    from nexus_web_eye import NexusWebEye
except ImportError:
    print("❌ Error: NexusWebEye not found or dependencies missing (Playwright).")
    print("Run: pip install playwright && playwright install chromium")
    sys.exit(1)

def main():
    print("🚀 INICIANDO PROTOCOLO DE VERIFICACION WEB LOCAL")
    
    # 1. Start Server
    server_process = None
    try:
        print("   Iniciando Servidor Flet (Puerto 8570)...")
        # Ensure port is free, or just launch and hope
        # Using verify_web_full.py as the server runner
        env = os.environ.copy()
        env["FLET_WEB_RENDERER"] = "canvaskit"
        
        server_cmd = [sys.executable, "verify_web_full.py"]
        # Use start_new_session to ensure it doesn't get killed with us immediately if on unix, but fine for win
        server_process = subprocess.Popen(server_cmd, cwd=os.getcwd(), env=env)
        
        print(f"   PID Servidor: {server_process.pid}")
        print("   ⏳ Esperando 60s para inicio completo (Deep Wait)...")
        time.sleep(60) 
        
        if server_process.poll() is not None:
             print(f"❌ El servidor murió prematuramente. Exit code: {server_process.returncode}")
             return

        # 2. Run Nexus Web Eye
        eye = NexusWebEye()
        # Ensure url is correct
        report = eye.verify_interface("http://localhost:8570")
        
        if report["success"]:
            print("\n✅ VERIFICACIÓN NAVEGADOR (Local) EXITOSA")
            print(f"   Elementos verificados: {report['checks']}")
        else:
            print("\n❌ FALLO EN VERIFICACIÓN")
            print(f"   Reporte: {report}")

    except Exception as e:
        print(f"❌ Error script principal: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 3. Cleanup
        if server_process:
            print("   📉 Deteniendo servidor web...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except:
                server_process.kill()
                print("   💀 Servidor asesinado (force kill).")

if __name__ == "__main__":
    main()
