import sys
import flet as ft
from main import main
import os

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

if __name__ == "__main__":
    try:
        with open("launch_start_log.txt", "w", encoding='utf-8') as f:
            f.write("Starting Web Launcher...\n")
        
        print("Re-Launching WEB Mode (Digital Eye)...", flush=True)
        
        # Agent needs WEB interface to see. User uses Desktop.
        # We launch on port 8575 for the agent.
        ft.run(main, view=ft.AppView.WEB_BROWSER, port=8577, web_renderer=ft.WebRenderer.CANVAS_KIT)
        
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        with open("launch_crash_log.txt", "w", encoding='utf-8') as f:
            f.write(f"CRASH: {e}\n{err}")
        print(f"CRASH: {e}", flush=True)
