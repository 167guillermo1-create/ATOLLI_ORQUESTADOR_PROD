import flet as ft
import inspect

try:
    with open("TABS_SIGNATURE.txt", "w") as f:
        f.write(f"VERSION: {ft.__version__}\n")
        f.write(f"SIG: {str(inspect.signature(ft.Tabs.__init__))}\n")
        f.write(f"DOC: {ft.Tabs.__doc__}\n")
except Exception as e:
    with open("TABS_SIGNATURE.txt", "w") as f:
        f.write(f"ERROR: {str(e)}")
