
import flet as ft
import sys
import traceback

def test():
    print("=== CRASH DIAGNOSTIC ===")
    print(f"Flet Version: {ft.__version__}")
    
    print("\n--- Checking WebRenderer ---")
    try:
        print(f"ft.WebRenderer content: {dir(ft.WebRenderer)}")
        print(f"ft.WebRenderer.HTML: {ft.WebRenderer.HTML}")
        print(f"ft.WebRenderer.CANVAS_KIT: {ft.WebRenderer.CANVAS_KIT}")
    except Exception as e:
        print(f"WebRenderer Error: {e}")
        
    print("\n--- Checking Google GenAI ---")
    try:
        import google.generativeai as genai
        print("Import successful (ignoring warnings)")
    except ImportError:
        print("Import failed: google.generativeai not found")
    except Exception as e:
        print(f"Import crashed: {e}")

    print("\n--- Attempting Minimal Run ---")
    try:
        def main(page: ft.Page):
            page.add(ft.Text("Hello"))
        
        # Test just instantiating the app logic without running server if possible,
        # but ft.app blocks. 
        # We will just print we are ready.
        print("Ready to run ft.app (skipped for diagnostic to avoid block)")
    except Exception as e:
        print(f"Setup Error: {e}")

if __name__ == "__main__":
    test()
