
import shutil
import os
import datetime

def create_backup():
    # Configuration
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"stable_verified_jan18_v0.80.2_{timestamp}"
    source_dir = os.getcwd()
    backup_root = os.path.join(source_dir, "backups")
    dest_dir = os.path.join(backup_root, backup_name)

    # Exclusions
    ignore_patterns = shutil.ignore_patterns(
        "__pycache__", 
        "*.pyc", 
        ".venv", 
        ".git", 
        "backups", 
        "*.log", 
        "verification_results",
        "*.png",
        "*.jpg"
    )

    print(f"Starting Backup...")
    print(f"Source: {source_dir}")
    print(f"Destination: {dest_dir}")

    try:
        shutil.copytree(source_dir, dest_dir, ignore=ignore_patterns)
        
        # Add a README to the backup
        readme_path = os.path.join(dest_dir, "BACKUP_INFO.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# Backup Information\n")
            f.write(f"**Date:** {datetime.datetime.now()}\n")
            f.write("**Status:** STABLE / VERIFIED\n")
            f.write("**Flet Version:** 0.80.2 (Strict)\n")
            f.write("**Renderer:** CanvasKit\n")
            f.write("**Description:** Full backup after fixing HTML renderer crash and shielding factory generation.\n")
            
        print(f"Backup created successfully at: {dest_dir}")
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

if __name__ == "__main__":
    create_backup()
