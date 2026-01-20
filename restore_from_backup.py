import os
import shutil
import sys
import subprocess

EXCLUDE_DIRS = {".venv", "backups", ".git", "__pycache__", ".idea", "vscode"}
EXCLUDE_FILES = {"restore_from_backup.py", "RESTAURAR_SISTEMA.bat", "create_backup.py"}

def list_backups():
    backup_root = os.path.join(os.getcwd(), "backups")
    if not os.path.exists(backup_root):
        return []
    
    # Filter only directories
    backups = [d for d in os.listdir(backup_root) if os.path.isdir(os.path.join(backup_root, d))]
    backups.sort(reverse=True) # Newest first
    return backups

def clean_workspace():
    """Safely cleans the workspace, preserving critical folders."""
    print("🧹 Cleaning current workspace...")
    root = os.getcwd()
    
    for item in os.listdir(root):
        if item in EXCLUDE_DIRS or item in EXCLUDE_FILES:
            continue
            
        path = os.path.join(root, item)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception as e:
            print(f"Warning: Could not delete {item}: {e}")

def restore_backup(backup_name):
    backup_path = os.path.join(os.getcwd(), "backups", backup_name)
    root = os.getcwd()
    
    print(f"♻️ Restoring from: {backup_name}...")
    
    # Copy all items from backup to root
    for item in os.listdir(backup_path):
        s = os.path.join(backup_path, item)
        d = os.path.join(root, item)
        
        # Don't overwrite exclusions if they exist in backup (optional, but safer to skip)
        if item in EXCLUDE_DIRS: 
            continue
            
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        except Exception as e:
            print(f"Error restoring {item}: {e}")

    print("✅ Files restored.")
    
    # Re-install dependencies
    if os.path.exists("requirements.txt"):
        print("📦 Re-syncing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=False)

def main():
    print("=== PHOENIX PROTOCOL: SYSTEM RESTORATION ===")
    print("Warning: This will OVERWRITE your current workspace files.")
    print("Excluded from deletion: backups/, .venv/, .git/\n")
    
    backups = list_backups()
    if not backups:
        print("❌ No backups found in /backups folder.")
        input("Press ENTER to exit...")
        return

    print("Available Backups:")
    for i, b in enumerate(backups):
        print(f"[{i+1}] {b}")
    
    print("\n[Q] Quit")
    
    choice = input("\nSelect backup to restore: ").strip().lower()
    if choice == 'q':
        return
        
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(backups):
            target = backups[idx]
            confirm = input(f"❗ Are you sure you want to restore '{target}'? (y/n): ")
            if confirm.lower() == 'y':
                clean_workspace()
                restore_backup(target)
                print("\n✨ SYSTEM RESTORATION COMPLETE ✨")
                print("You may need to restart the application.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")
    
    input("\nPress ENTER to exit...")

if __name__ == "__main__":
    main()
