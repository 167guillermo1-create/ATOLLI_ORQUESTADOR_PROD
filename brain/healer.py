import os
import subprocess
import sys
import re

class HealerAgent:
    """
    The White Mage. 
    Receives pain reports and administers treatment.
    """
    
    def __init__(self):
        self.treatment_log = []

    def diagnose(self, pain_report):
        """
        Returns a treatment plan (function, args) based on the pain report.
        """
        error_type = pain_report.get("type")
        raw_error = pain_report.get("raw_error", "")
        
        print(f"🚑 HEALER: Diagnosing {error_type}...")
        
        if error_type == "IMPORT":
            return self._treat_import_error(raw_error)
        elif error_type == "SYNTAX":
            return self._treat_syntax_error(raw_error)
        else:
            return None, "Unknown ailment. Manual intervention required."

    def heal(self, treatment_plan):
        """
        Executes the treatment.
        """
        func, args = treatment_plan
        if func:
            print(f"💉 HEALER: Applying treatment -> {func.__name__}")
            return func(*args)
        else:
            print("💀 HEALER: No treatment available.")
            return False

    # --- TREATMENTS ---

    def _treat_import_error(self, error_text):
        """
        Extracts missing module name and installs it.
        """
        # Pattern: "No module named 'xyz'"
        match = re.search(r"No module named ['\"]([^'\"]+)['\"]", error_text)
        if match:
            module_name = match.group(1)
            return self._install_package, [module_name]
        return None, "Could not identify module name."

    def _install_package(self, package_name):
        """
        Treatment: pip install <package>
        """
        try:
            print(f"💊 HEALER: Prescribing 'pip install {package_name}'")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            return True
        except subprocess.CalledProcessError:
            print(f"💔 HEALER: Treatment failed. Could not install {package_name}.")
            return False

    def _treat_syntax_error(self, error_text):
        # Placeholder for complex LLM-based code fixing
        # In a real scenario, this would call the Brain to rewrite the file.
        print("⚠️ HEALER: Syntax Error requires surgical intervention (LLM Edit). Not yet implemented.")
        return None, "Surgery required."
