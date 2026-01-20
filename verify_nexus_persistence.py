import os
import sys

# Setup paths
sys.path.append(os.path.join(os.getcwd(), "brain"))

from main import AgentOrchestrator

def verify_persistence():
    data_dir = os.path.join(os.getcwd(), "data")
    env_path = os.path.join(data_dir, ".env")
    
    agent = AgentOrchestrator(env_path)
    
    print("--- Testing Persistence ---")
    print(f"Current Total Tokens: {agent.usage_stats['tokens_total']}")
    
    # Mock some usage
    agent.usage_stats['tokens_total'] += 100
    agent.usage_stats['cost_usd'] += 0.005
    agent.usage_stats['providers']['groq']['tokens'] += 100
    agent.usage_stats['providers']['groq']['cost'] += 0.005
    
    print(f"Updated Tokens (Mock): {agent.usage_stats['tokens_total']}")
    
    # Save
    agent.save_nexus_state()
    print("State saved.")
    
    # Reload
    agent2 = AgentOrchestrator(env_path)
    print(f"Reloaded Tokens: {agent2.usage_stats['tokens_total']}")
    
    if agent2.usage_stats['tokens_total'] == agent.usage_stats['tokens_total']:
        print("✅ SUCCESS: Persistence verified.")
    else:
        print("❌ FAILURE: Persistence failed.")

if __name__ == "__main__":
    print("🚀 Starting Persistence Test...")
    try:
        verify_persistence()
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
