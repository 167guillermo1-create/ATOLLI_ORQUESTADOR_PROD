import flet as ft
import inspect
import sys

print(f"PYTHON: {sys.version}")
print(f"FLET: {ft.__version__}")

try:
    print("TABS __INIT__:")
    print(inspect.signature(ft.Tabs.__init__))
except Exception as e:
    print(f"ERROR TABS: {e}")

try:
    print("TAB __INIT__:")
    print(inspect.signature(ft.Tab.__init__))
except Exception as e:
    print(f"ERROR TAB: {e}")

print("TABS DIR:")
print([a for a in dir(ft.Tabs) if not a.startswith("_")])
