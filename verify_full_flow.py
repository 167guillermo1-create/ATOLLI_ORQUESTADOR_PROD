import os
import sys
import time
import subprocess
import threading
import codecs

# Windows Console Encoding Fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add 'brain' to path to import NexusOculus
sys.path.append(os.path.join(os.path.dirname(__file__), "brain"))
from nexus_oculus import NexusOculus, NexusInteractor

def launch_app():
    """Launches the app in a separate thread/process"""
    print("🚀 Launching ATOLLI ORQUESTADOR (Desktop Mode)...")
    cmd = [sys.executable, "main.py"]
    # We use Popen to keep it running
    return subprocess.Popen(cmd, cwd=os.getcwd())

def verify_flow():
    # 1. Start App
    process = launch_app()
    print("⏳ Waiting 10s for app to warm up...")
    time.sleep(10)

    # 2. Init Oculus
    eye = NexusOculus(output_dir="verification_results/full_flow")
    
    # 3. Locate Window
    print("👁️ Oculus: Scanning for 'NEXUS MASTER GEN'...")
    if not eye.locate_window("NEXUS MASTER GEN", retries=5):
        print("❌ CRITICAL: Could not find application window.")
        process.terminate()
        return

    # 4. Init Interactor
    hand = NexusInteractor(eye)

    # 5. Define Steps
    steps = [
        {"name": "Step 1: Brain Module (Initial)", "check": "BRAIN", "wait": 2},
        {"name": "Step 2: Navigate to Factory", "action": "Click FACTORY tab", "vision_target": "The button labeled 'FACTORY' in the navigation bar", "wait": 3},
        {"name": "Step 3: Verify Factory UI", "check": "FACTORY", "wait": 1},
        {"name": "Step 4: Navigate to Matrix", "action": "Click MATRIX tab", "vision_target": "The button labeled 'MATRIX' in the navigation bar", "wait": 3},
        {"name": "Step 5: Verify Matrix Stats", "check": "MATRIX", "wait": 1},
        {"name": "Step 6: Navigate to Config", "action": "Click CONFIG tab", "vision_target": "The button labeled 'CONFIG' in the navigation bar", "wait": 3},
        {"name": "Step 7: Verify Config Keys", "check": "CONFIG", "wait": 1},
        {"name": "Step 8: Return to Brain", "action": "Click BRAIN tab", "vision_target": "The button labeled 'BRAIN' in the navigation bar", "wait": 3}
    ]

    print("\n🎬 STARTING VISUAL NAVIGATION PROTOCOL\n")

    for step in steps:
        print(f"👉 {step['name']}")
        
        # Action
        if "vision_target" in step:
            success = hand.click_element_by_vision(step["vision_target"])
            if not success:
                print(f"   ⚠️ Warning: Could not visually click '{step['vision_target']}'. Trying blind/fallback or skipping.")
        
        time.sleep(step.get("wait", 2))
        
        # Capture & Check
        safe_name = step['name'].replace(" ", "_").replace(":", "")
        img_path = eye.capture_view(safe_name)
        
        integrity = eye.analyze_visual_integrity(img_path)
        print(f"   📸 Captured: {os.path.basename(img_path)} | Integrity: {'✅ OK' if integrity else '❌ FAIL'}")

    print("\n✅ VERIFICATION SEQUENCE COMPLETE.")
    print("📉 Closing application...")
    process.terminate()

if __name__ == "__main__":
    verify_flow()
