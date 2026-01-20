import flet as ft
import inspect

print(f"Flet Version: {ft.version}")

try:
    sig = inspect.signature(ft.Icon.__init__)
    print(f"Icon.__init__ signature: {sig}")
except Exception as e:
    print(f"Error getting signature: {e}")

try:
    print("Testing ft.Icon('add')...")
    i = ft.Icon("add")
    print("Success positional")
except Exception as e:
    print(f"Error positional: {e}")

try:
    print("Testing ft.Icon(name='add')...")
    i = ft.Icon(name="add")
    print("Success keyword 'name'")
except Exception as e:
    print(f"Error keyword 'name': {e}")
