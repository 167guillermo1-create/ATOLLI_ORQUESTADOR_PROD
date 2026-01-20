import flet as ft
import inspect

def diagnose():
    with open("flet_diagnostic_results.txt", "w") as f:
        f.write("=== FLET VERSION ===\n")
        f.write(f"{ft.__version__}\n\n")
        
        f.write("=== Tab.__init__ Signature ===\n")
        f.write(str(inspect.signature(ft.Tab.__init__)) + "\n\n")
        
        f.write("=== Tab Attributes ===\n")
        f.write("\n".join([a for a in dir(ft.Tab) if not a.startswith("_")]) + "\n\n")
        
        f.write("=== Tabs.__init__ Signature ===\n")
        f.write(str(inspect.signature(ft.Tabs.__init__)) + "\n\n")
        
        f.write("=== Tabs Attributes ===\n")
        f.write("\n".join([a for a in dir(ft.Tabs) if not a.startswith("_")]))

if __name__ == "__main__":
    diagnose()
