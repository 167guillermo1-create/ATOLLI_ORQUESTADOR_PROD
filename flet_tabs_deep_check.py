import flet as ft
import inspect
import sys
import traceback

print("--- FLET INTROSPECTION ---")
print(f"Version: {ft.__version__}")

def get_info(obj):
    name = str(obj)
    print(f"\nAnalyzing: {name}")
    try:
        sig = inspect.signature(obj.__init__)
        print(f"Signature: {sig}")
    except Exception as e:
        print(f"Error getting signature: {e}")
    
    print("Members:")
    members = [m for m in dir(obj) if not m.startswith("_")]
    print(members)

get_info(ft.Tabs)
get_info(ft.Tab)

# Try to find if there is a 'controls' or 'tabs' property in the class itself
print("\nIs 'controls' in ft.Tabs?", hasattr(ft.Tabs, "controls"))
print("Is 'tabs' in ft.Tabs?", hasattr(ft.Tabs, "tabs"))

# Try to instantiate with the suggested error fix
print("\nTrial instantiation...")
try:
    # Just a guess based on the error: ft.Tabs(content=Control, length=Int)
    # But usually positional means ft.Tabs(content, length)
    t = ft.Tabs(ft.Container(), 3)
    print("Success with ft.Tabs(Container, 3)")
except Exception:
    traceback.print_exc()

# Let's see what ft.Tabs really is
print(f"Tabs Base Classes: {ft.Tabs.__mro__}")
