import flet as ft
import inspect
import sys

with open("FINAL_DIAGNOSTIC.txt", "w") as f:
    f.write(f"VERSION: {ft.__version__}\n")
    try:
        sig = inspect.signature(ft.Tabs.__init__)
        f.write(f"TABS_SIG: {sig}\n")
    except Exception as e:
        f.write(f"TABS_ERR: {e}\n")
    
    f.write(f"TABS_DOC: {ft.Tabs.__doc__}\n")
    f.write(f"TABS_DIR: {dir(ft.Tabs)}\n")
