import flet as ft

def test():
    potential_props = ['content', 'body', 'child', 'view', 'tab_content']
    print(f"Flet Version: {ft.__version__}")
    for p in potential_props:
        try:
            ft.Tab(**{p: ft.Container()})
            print(f"{p}: OK")
        except TypeError as e:
            print(f"{p}: FAIL - {e}")

if __name__ == "__main__":
    test()
