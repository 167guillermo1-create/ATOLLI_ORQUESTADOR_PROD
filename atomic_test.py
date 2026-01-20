import flet as ft

def main(page: ft.Page):
    print("ATOMIC TEST: Starting")
    
    # PASO 1: Setup básico (esto funcionó en level0)
    page.title = "ATOMIC TEST"
    page.bgcolor = "black"
    page.update()
    print("PASO 1: Page configured")
    
    # PASO 2: Agregar UN texto
    page.add(ft.Text("PASO 2: Text agregado", color="green", size=20))
    page.update()
    print("PASO 2: Text added")
    
    # PASO 3: Agregar UN Container
    page.add(ft.Container(
        content=ft.Text("PASO 3: Container agregado", color="yellow"),
        bgcolor="#111111",
        padding=10
    ))
    page.update()
    print("PASO 3: Container added")
    
    # PASO 4: Agregar UNA Column
    page.add(ft.Column([
        ft.Text("PASO 4: Column agregada", color="cyan"),
        ft.Text("Item 2 de Column", color="cyan")
    ]))
    page.update()
    print("PASO 4: Column added")
    
    # PASO 5: Agregar UN TextField
    page.add(ft.TextField(hint_text="PASO 5: TextField", color="white"))
    page.update()
    print("PASO 5: TextField added")
    
    print("ATOMIC TEST: Completado - Si ves este mensaje, todos los pasos funcionaron")

if __name__ == "__main__":
    print("=== ATOMIC TEST ===")
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press ENTER...")
