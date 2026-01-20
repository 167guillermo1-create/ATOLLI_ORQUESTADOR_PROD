import sys
import flet as ft
from main import main
import os

sys.stdout.reconfigure(line_buffering=True)

if __name__ == "__main__":
    print("🚀 Re-Launching WEB Mode (Safe HTML Renderer)...", flush=True)
    try:
        # Use HTML renderer to avoid "White Screen" in headless environments
        ft.app(
            target=main, 
            view=ft.AppView.WEB_BROWSER, 
            port=8555, 
            web_renderer=ft.WebRenderer.HTML,
            open_browser=False
        )
    except Exception as e:
        print(f"CRASH: {e}", flush=True)
