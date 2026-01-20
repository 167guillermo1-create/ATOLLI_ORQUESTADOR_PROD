
import os
import subprocess
import time
import sys
from brain.nexus_oculus import NexusOculus

def launch_and_verify():
    print("Launching ATOLLI NEXUS Desktop for Verification...")
    
    # Path to main.py
    main_script = os.path.abspath("main.py")
    
    # Launch in a subprocess
    process = subprocess.Popen([sys.executable, main_script], cwd=os.getcwd())
    
    print(f"Waiting for application to load (PID: {process.pid})...")
    # Wait longer for Flet to fully render
    time.sleep(10) 
    
    # Initialize Digital Eye
    output_dir = "verification_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    eye = NexusOculus(output_dir=output_dir)
    
    # Attempt to locate
    # Flet window titles can vary, usually "Flet" or the app name
    found = eye.locate_window("NEXUS MASTER GEN", retries=5) or eye.locate_window("Flet", retries=2)
    
    exit_code = 0
    
    if found:
        print("Window identified.")
        # Capture initial state
        screenshot = eye.capture_view("initial_load")
        
        # Analyze
        valid = eye.analyze_visual_integrity(screenshot)
        if valid:
            print("Visual Integrity Check: PASS")
        else:
            print("Visual Integrity Check: FAIL (Image might be empty)")
            exit_code = 1
            
    else:
        print("Could not find window. Capturing full screen for debug.")
        eye.capture_view("debug_not_found")
        exit_code = 1
    
    print("Closing application in 5 seconds...")
    time.sleep(5)
    process.terminate()
    print(f"Test Complete. Exit Code: {exit_code}")
    sys.exit(exit_code)

if __name__ == "__main__":
    launch_and_verify()
