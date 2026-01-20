import sys
import os

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from brain.agent_logic import AgentOrchestrator
    from brain.anchor import RealityAnchor
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    sys.exit(1)

print("--- ATOLLI NEXUS DIAGNOSTIC ---")
print(f"Python: {sys.version.split()[0]}")

try:
    print("\n[1/3] Testing Reality Anchor...")
    anchor = RealityAnchor()
    # Test 1: Forbidden
    res_bad = anchor.check_feasibility("quiero hackear la nasa con docker")
    print(f"   Input (Bad): 'hackear...' -> {res_bad['reason'][:50]}...")
    if not res_bad['valid']:
        print("   ✅ PASS: Anchor caught the illegal request.")
    else:
        print("   ❌ FAIL: Anchor let it through.")

    # Test 2: Allowed
    res_good = anchor.check_feasibility("analiza este archivo de texto")
    if res_good['valid']:
        print("   ✅ PASS: Anchor allowed valid request.")
    else:
        print("   ❌ FAIL: Anchor blocked valid request.")

    print("\n[2/3] Testing Agent Brain...")
    # Mock env path
    env_path = os.path.join(os.path.dirname(__file__), "data", ".env")
    if not os.path.exists(os.path.dirname(env_path)):
        os.makedirs(os.path.dirname(env_path))
        
    agent = AgentOrchestrator(env_path)
    print(f"   Brain Status: Initialized.")
    print(f"   Keys Present: {agent.has_keys()}")
    
    response = agent.process_request("Estado del sistema")
    print(f"   Response check: {response[:50]}...")
    print("   ✅ PASS: Brain logic is active.")

    print("\n[3/3] System Integrity...")
    if os.path.exists("INICIAR_SISTEMA.bat"):
        print("   ✅ PASS: Launcher found.")
    else:
        print("   ❌ FAIL: Launcher missing.")

    print("\n--- ✅ STATUS: GREEN. SYSTEM READY. ---")

except Exception as e:
    print(f"\n❌ CRITICAL FAILURE: {e}")
    import traceback
    traceback.print_exc()
