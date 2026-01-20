import flet as ft
import sys

def main(page: ft.Page):
    print("LEVEL 0: Init")
    page.title = "DIAGNOSTIC LEVEL 0"
    page.bgcolor = "black"
    page.update()
    
    print("LEVEL 0: Page Configured")
    
    try:
        t = ft.Text("SI PUEDES LEER ESTO, FLET FUNCIONA.", color="green", size=30)
        page.add(t)
        page.update()
        print("LEVEL 0: Text Added")
    except Exception as e:
        print(f"LEVEL 0 ERROR: {e}")

if __name__ == "__main__":
    print("--- STARTING DIAGNOSTIC LEVEL 0 ---")
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"CRITICAL: {e}")
        input("Press Enter...")
