import flet as ft
try:
    print(f"Flet version: {ft.version}")
except:
    print("Could not get flet version")

print("\n--- ft.Alignment dir ---")
try:
    print(dir(ft.Alignment))
except Exception as e:
    print(e)

print("\n--- ft.alignment dir ---")
try:
    print(dir(ft.alignment))
except Exception as e:
    print(e)

print("\n--- ft.Alignment.top_left check ---")
try:
    print(ft.Alignment.top_left)
except Exception as e:
    print(e)

print("\n--- ft.alignment.top_left check ---")
try:
    print(ft.alignment.top_left)
    print(ft.alignment.TOP_LEFT)
except Exception as e:
    print(e)
