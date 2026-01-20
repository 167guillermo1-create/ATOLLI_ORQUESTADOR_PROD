import flet as ft
import os
import sys

# Ensure backend path
sys.path.append(os.path.join(os.getcwd(), "brain"))

from main import main

if __name__ == "__main__":
    print("🚀 LAUNCHING NEXUS MASTER GEN (WEB MODE) ON PORT 8570...")
    try:
        # Force CanvasKit for better compatibility with headless browsers/automation
        ft.app(target=main, port=8570, view=ft.AppView.WEB_BROWSER, web_renderer="canvaskit")
    except Exception as e:
        print(f"❌ CRITICAL LAUNCH ERROR: {e}")
        input("Press Enter to exit...")
