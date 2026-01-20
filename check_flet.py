import flet as ft
import sys

print(f"Flet Version: {ft.version}")
try:
    print(f"ft.alignment: {ft.alignment}")
    print(f"Has top_left? {hasattr(ft.alignment, 'top_left')}")
    print(f"Dir: {dir(ft.alignment)}")
except Exception as e:
    print(f"Error inspecting alignment: {e}")
