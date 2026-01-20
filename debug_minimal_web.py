
import flet as ft
import sys

def main(page: ft.Page):
    print("PAGE CONNECTED")
    page.add(ft.Text("Hello World"))

if __name__ == "__main__":
    print("STARTING SERVER ON 8560...")
    try:
        ft.app(target=main, port=8560, view=ft.AppView.WEB_BROWSER)
    except Exception as e:
        print(f"ERROR: {e}")
