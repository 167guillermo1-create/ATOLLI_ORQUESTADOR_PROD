
import os
import sys
import json
import time
import subprocess

# Import Sibling Intelligence Modules
try:
    from anchor import NexusHealer
    from qa_arbiter import QAArbiter
except ImportError:
    # Fix path if running directly
    sys.path.append(os.path.dirname(__file__))
    from anchor import NexusHealer
    from qa_arbiter import QAArbiter

# Windows Console Encoding Fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

class HealerLoop:
    """
    Autonomous Loop (Self-Healing):
    1. ARBITER: Checks code static logic (QA).
    2. RUNNER: Launches Test Suite.
    3. HEALER: Attempts Mechanical Fixes if failure.
    """
    def __init__(self, target_file="main.py"):
        self.target_file = os.path.abspath(target_file)
        self.test_runner = "desktop_test_suite.py" # Or verify_full_flow.py
        self.report_path = os.path.join("verification_results", "test_report.json")
        self.max_retries = 3
        self.arbiter = QAArbiter()
        self.healer = NexusHealer()

    def run_cycle(self):
        print("\n⚡ STARTING HEALER LOOP CYCLE ⚡")
        
        for attempt in range(self.max_retries):
            print(f"\n🔄 CYCLE {attempt + 1}/{self.max_retries}")
            
            # PHASE 1: STATIC PRE-CHECK (QA ARBITER)
            print("🔍 [PHASE 1] QA Arbiter Static Analysis...")
            if os.path.exists(self.target_file):
                with open(self.target_file, "r", encoding="utf-8") as f:
                    code = f.read()
                
                check = self.arbiter.audit_code_logic(code)
                if not check["success"]:
                    print(f"   ⚠️ QA Issues Detected: {check['errors']}")
                    # Should we fix immediately? 
                    # For now, we note it. The Healer might fix it if it causes a crash.
                else:
                    print("   ✅ QA Check Passed.")
            
            # PHASE 2: DYNAMIC EXECUTION (TEST SUITE)
            print(f"🚀 [PHASE 2] Executing Tests ({self.test_runner})...")
            cmd = [sys.executable, self.test_runner]
            
            with open("healer_log.txt", "w") as log:
                # Run with timeout to prevent hangs
                try:
                    subprocess.run(cmd, stdout=log, stderr=log, timeout=60)
                except subprocess.TimeoutExpired:
                    print("   ❌ Timeout Detected.")
            
            # PHASE 3: ANALYSIS
            # We check the test report OR the exit code logic (if runner saves report)
            success = self.analyze_results()
            
            if success:
                print("\n✅ SYSTEM NOMINAL. LOOP COMPLETE.")
                return True
            
            # PHASE 4: MECHANICAL HEALING
            print("🔧 [PHASE 4] Attempting Mechanical Repair...")
            self.apply_healing()
            time.sleep(1) # Wait for FS write
            
        print("\n❌ CRITICAL: Max retries reached. Human Intervention Required.")
        return False

    def analyze_results(self):
        if not os.path.exists(self.report_path):
            # Fallback: Check log for simple success keywords
            if os.path.exists("healer_log.txt"):
                with open("healer_log.txt", "r") as f:
                    content = f.read()
                if "OK" in content or "PASSED" in content or "Exit Code: 0" in content:
                    return True
            return False
            
        try:
            with open(self.report_path, "r") as f:
                data = json.load(f)
            return data.get("status") == "success" or data.get("status") == "PASS"
        except:
            return False

    def apply_healing(self):
        """Reads target, heals it, saves it."""
        try:
            with open(self.target_file, "r", encoding="utf-8") as f:
                original_code = f.read()
            
            # Apply Mechanical Fixes (Firmware Rules)
            healed_code = self.healer.heal_code(original_code)
            
            if original_code != healed_code:
                with open(self.target_file, "w", encoding="utf-8") as f:
                    f.write(healed_code)
                print("   🩹 Patch Applied (Firmware Match).")
            else:
                print("   ⚠️ No mechanical fixes found for current code state.")
                
        except Exception as e:
            print(f"   ❌ Healing Error: {e}")

if __name__ == "__main__":
    # Default target is main.py in project root
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    loop = HealerLoop(target)
    loop.run_cycle()
