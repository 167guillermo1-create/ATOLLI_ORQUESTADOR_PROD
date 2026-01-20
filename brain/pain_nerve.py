import subprocess
import traceback
import sys
import re
import os

class PainNerve:
    """
    The sensory system for the AI. 
    Captures errors, classifies them, and prepares them for the Healer.
    """
    
    ERROR_TYPES = {
        "SYNTAX": r"SyntaxError|IndentationError|TabError",
        "IMPORT": r"ModuleNotFoundError|ImportError",
        "LOGIC": r"NameError|TypeError|ValueError|IndexError|KeyError|AttributeError",
        "SYSTEM": r"OSError|RuntimeError|ConnectionError|Timeout"
    }

    @staticmethod
    def classify_error(error_text):
        """
        Analyzes the error text and assigns a category.
        """
        for err_type, pattern in PainNerve.ERROR_TYPES.items():
            if re.search(pattern, error_text):
                return err_type
        return "UNKNOWN"

    @staticmethod
    def capture_exec(command, cwd=None):
        """
        Runs a command safely and captures any 'pain' (stderr).
        Returns: (success, output, error_report)
        """
        try:
            # Enforce UTF-8 for Windows consistency
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"

            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                env=env,
                check=False # We handle return codes manually
            )
            
            if result.returncode == 0:
                return True, result.stdout, None
            else:
                # PAIN DETECTED
                error_body = result.stderr if result.stderr else result.stdout
                classification = PainNerve.classify_error(error_body)
                
                pain_report = {
                    "type": classification,
                    "raw_error": error_body,
                    "command": command,
                    "return_code": result.returncode
                }
                return False, result.stdout, pain_report

        except Exception as e:
            # Meta-pain (Execution failed completely)
            return False, "", {
                "type": "SYSTEM",
                "raw_error": str(e),
                "command": command,
                "meta_exception": traceback.format_exc()
            }
