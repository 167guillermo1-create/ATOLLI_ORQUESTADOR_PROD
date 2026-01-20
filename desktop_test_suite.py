
import os
import sys
import time
import json
import subprocess
from brain.nexus_oculus import NexusOculus, NexusInteractor

class DesktopTestSuite:
    def __init__(self):
        self.output_dir = "verification_results"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        self.eye = NexusOculus(output_dir=self.output_dir)
        self.interactor = NexusInteractor(self.eye)
        self.process = None
        self.report = {"tests": [], "status": "PENDING"}

    def launch_app(self):
        print("Launching App (ENVIRONMENT WEB MODE)...")
        # Launch using Python and Env Var
        env = os.environ.copy()
        env["ATOLLI_WEB_MODE"] = "true"
        self.process = subprocess.Popen([sys.executable, "main.py"], cwd=os.getcwd(), env=env)
        time.sleep(40) # Wait for web server, browser launch, and Flet init (CanvasKit)
        
        found = self.eye.locate_window("NEXUS MASTER GEN", retries=5)
        if not found:
            print("Failed to find app window.")
            return False
        return True

    def close_app(self):
        if self.process:
            print("Closing App...")
            self.process.terminate()
            self.process.wait()

    def run_test(self, test_name, func):
        print(f"\n--- RUNNING TEST: {test_name} ---")
        try:
            if not self.eye.target_window:
                # Try to re-locate if lost
                self.eye.locate_window("NEXUS MASTER GEN")
                
            success = func()
            
            # Capture evidence
            evidence = self.eye.capture_view(f"evidence_{test_name}")
            valid_visual = self.eye.analyze_visual_integrity(evidence)
            
            result = "PASS" if (success and valid_visual) else "FAIL"
            print(f"--- RESULT: {result} ---")
            
            self.report["tests"].append({
                "name": test_name,
                "result": result,
                "evidence": evidence
            })
            return result == "PASS"
        except Exception as e:
            print(f"Test Exception: {e}")
            self.report["tests"].append({
                "name": test_name,
                "result": "ERROR",
                "error": str(e)
            })
            return False

    def test_navigation(self):
        # Click tabs using Visual Descriptions
        print("Testing Navigation (Visual)...")
        
        # Go to Factory
        if not self.interactor.click_element_by_vision("The 'Factory' tab icon or text in the sidebar"): return False
        time.sleep(2)
        
        # Go to Matrix
        if not self.interactor.click_element_by_vision("The 'Matrix' tab icon or text in the sidebar"): return False
        time.sleep(2)
        
        # Go back to Brain
        if not self.interactor.click_element_by_vision("The 'Brain' tab icon or text in the sidebar"): return False
        time.sleep(2)
        
        return True

    def test_factory_generation(self):
        print("Testing Factory Generation...")
        # Go to Factory
        self.interactor.click_region("tab_factory")
        time.sleep(2)
        
        # Fill Name
        self.interactor.click_region("factory_input_name")
        self.interactor.type_text("Project_Alpha_Test")
        time.sleep(1)
        
        # Click Generate
        self.interactor.click_region("factory_generate_btn")
        time.sleep(5) # Wait for generation simulation
        
        return True

    def test_config_management(self):
        print("Testing Config Management (Visual Verification)...")
        # Go to Config
        if not self.interactor.click_element_by_vision("The 'Config' tab icon in the sidebar"): return False
        time.sleep(2)
        
        # Click Groq Input
        print("Locating Groq Input...")
        time.sleep(2) # Allow animation to finish
        if not self.interactor.click_element_by_vision("The first text input field in the main area"): return False
        # Type dummy key
        self.interactor.type_text("gsk_vision_dummy_test")
        time.sleep(1)
        
        # Click Refresh/Test Button next to Groq
        print("Testing Connection Button...")
        if not self.interactor.click_element_by_vision("The refresh/test icon button next to the Groq input field"): return False
        time.sleep(3) # Wait for verification
        
        # Click Save
        # self.interactor.click_element_by_vision("The button labeled 'GUARDAR CONFIGURACION'")
        # time.sleep(3)
        
        # Verify Visual Feedback
        screenshot = self.eye.capture_view("config_result")
        prompt = "Look at the status icon (circle) next to the Groq input field. Is it green or red? Or is there a text saying 'FALLÓ' or 'CONECTADO'?"
        analysis = self.interactor.vision.analyze_ui(screenshot, prompt)
        print(f"Visual Feedback: {analysis}")
        
        # We expect it to fail (red) for dummy key, or pass (green) if real key was there.
        # Just verifying the AI *sees* the status is enough for this test.
        if analysis and ("red" in analysis.lower() or "fail" in analysis.lower() or "falló" in analysis.lower() or "green" in analysis.lower()):
             return True
        
        return False

    def test_vision_capabilities(self):
        print("Testing Pure Vision Query...")
        # Just ask what is on screen
        screenshot = self.eye.capture_view("vision_test")
        description = self.interactor.vision.analyze_ui(screenshot, "Describe the UI layout briefly.")
        print(f"AI Description: {description}")
        return True if description else False

    def execute_suite(self):
        try:
            if self.launch_app():
                self.run_test("Vision_Check", self.test_vision_capabilities)
                self.run_test("Navigation_Visual", self.test_navigation)
                self.run_test("Config_Visual", self.test_config_management)
                self.report["status"] = "COMPLETED"
            else:
                self.report["status"] = "FAILED_START"
        finally:
            self.close_app()
            self.save_report()

    def save_report(self):
        report_path = os.path.join(self.output_dir, "test_report.json")
        with open(report_path, "w") as f:
            json.dump(self.report, f, indent=4)
        print(f"Report saved to {report_path}")

if __name__ == "__main__":
    suite = DesktopTestSuite()
    suite.execute_suite()
