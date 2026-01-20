import subprocess
import sys
import time
import os

sys.stdout.reconfigure(encoding='utf-8')

def run_test(script_name):
    print(f"\n{'='*60}")
    print(f"RUNNING TEST: {script_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    # Use the same python interpreter
    python_exe = sys.executable
    
    try:
        # Run via subprocess to isolate contexts
        result = subprocess.run(
            [python_exe, script_name], 
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        duration = time.time() - start_time
        
        print(result.stdout)
        if result.stderr:
            print("--- STDERR ---")
            print(result.stderr)
            
        if result.returncode == 0:
            print(f"[PASSED] {script_name} in {duration:.2f}s")
            return True
        else:
            print(f"[FAILED] {script_name} with code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Execution Error: {e}")
        return False

def main():
    print(f"STARTING FINAL SYSTEM CHECK (Chapters 1-3)\n")
    
    scripts = [
        "test_ui_headless.py",          # Chapter 1: UI Logic & Brain
        "test_responsive_components.py",# Chapter 3: Luxury UI Components
        "verify_rpc_client.py",         # Chapter 2: Supabase RPC
        "test_factory_provisioning.py"  # Chapter 2: Factory
    ]
    
    passed = 0
    failed = 0
    
    for script in scripts:
        if run_test(script):
            passed += 1
        else:
            failed += 1
            
    print(f"\n{'='*60}")
    print(f"SYSTEM SUMMARY")
    print(f"{'='*60}")
    print(f"Tests Passed: {passed}")
    print(f"Tests Failed: {failed}")
    
    if failed == 0:
        print("\n[SUCCESS] SYSTEM INTEGRITY VERIFIED (GREEN)")
        sys.exit(0)
    else:
        print("\n[FAILURE] SYSTEM ISSUES DETECTED (RED)")
        sys.exit(1)

if __name__ == "__main__":
    main()
