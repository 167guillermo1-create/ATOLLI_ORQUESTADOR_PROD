import os
from playwright.sync_api import sync_playwright

class NexusWebEye:
    """
    Agente de Verificación Web Local (Playwright).
    Evita restricciones de API y verifica la UI real en localhost.
    """
    def __init__(self, output_dir="verification_results/web_flow"):
        self.output_dir = os.path.abspath(output_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def verify_interface(self, url="http://localhost:8570"):
        print(f"🕸️ NexusWebEye: Iniciando secuencia en {url}...")
        
        report = {"success": False, "checks": []}
        
        try:
            with sync_playwright() as p:
                # Launch Chromium Headless (or headed for debug if needed)
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # DEBUG: Capture Console & Errors
                page.on("console", lambda msg: print(f"   [BROWSER CONSOLE] {msg.text}"))
                page.on("pageerror", lambda exc: print(f"   [BROWSER ERROR] {exc}"))
                
                # 1. Navigate
                print("   Navegando...")
                page.goto(url)
                
                # 2. Wait for loading (Flet usually has a loading animation)
                # We wait for the main content to appear or loading to vanish
                try:
                    # Wait for Brain Title
                    page.wait_for_selector("text=BRAIN", timeout=60000)
                    print("   ✅ Elemento 'BRAIN' detectado.")
                    report["checks"].append("BRAIN_VISIBLE")
                    
                    # Wait for GlassInput (Placeholder)
                    # Playwright pseudo-class for placeholder or attribute selector
                    page.wait_for_selector("[placeholder='Comando Nexus...']", timeout=30000)
                    print("   ✅ GlassInput ('Comando Nexus...') detectado.")
                    report["checks"].append("GLASS_INPUT_VISIBLE")
                except Exception as exWait:
                    print(f"   ⚠️ Timeout esperando elementos UI: {exWait}")
                    
                # 3. Validar Elementos Clave
                content = page.content()
                for keyword in ["FACTORY", "MATRIX", "CONFIG"]:
                    if keyword in content:
                        print(f"   ✅ Texto '{keyword}' encontrado.")
                        report["checks"].append(f"{keyword}_VISIBLE")
                    else:
                        print(f"   ❌ Texto '{keyword}' NO encontrado.")
                
                # 4. Captura de Evidencia
                screenshot_path = os.path.join(self.output_dir, "web_verification_snapshot.png")
                page.screenshot(path=screenshot_path)
                print(f"   📸 Captura guardada: {screenshot_path}")
                
                browser.close()
                report["success"] = len(report["checks"]) >= 3 # At least 3 keywords
                
        except Exception as e:
            print(f"❌ Error en NexusWebEye: {e}")
            report["error"] = str(e)
            
        return report

if __name__ == "__main__":
    eye = NexusWebEye()
    eye.verify_interface()
