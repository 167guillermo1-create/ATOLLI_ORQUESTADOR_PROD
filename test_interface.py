"""
FLET COMPATIBILITY TEST - INTERFAZ VISUAL
Ejecuta tests de compatibilidad con interfaz gráfica
"""
import flet as ft
import sys

class TestRunner:
    def __init__(self):
        self.results = {
            "version": None,
            "tests": {}
        }
    
    def run_test(self, test_name, test_func):
        """Ejecuta un test y registra resultado"""
        try:
            test_func()
            self.results["tests"][test_name] = {"status": "PASS", "error": None}
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            return False

def main(page: ft.Page):
    page.title = "FLET COMPATIBILITY TESTER"
    page.bgcolor = "#050505"
    page.padding = 30
    page.window_width = 800
    page.window_height = 600
    
    runner = TestRunner()
    
    # Detectar versión
    try:
        runner.results["version"] = ft.__version__
    except:
        runner.results["version"] = "UNKNOWN"
    
    # UI Elements
    version_text = ft.Text(
        f"Flet Version: {runner.results['version']}", 
        size=16, 
        color="#00f2ff",
        weight="bold"
    )
    
    test_results = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    status_text = ft.Text("Listo para iniciar tests", color="white", size=14)
    
    def add_result(test_name, passed, error=None):
        """Agrega resultado visual"""
        icon_color = "green" if passed else "red"
        icon_name = "check_circle" if passed else "cancel"
        
        result_row = ft.Row([
            ft.Icon(icon_name, color=icon_color, size=20),
            ft.Column([
                ft.Text(test_name, color="white", weight="bold"),
                ft.Text(error if error else "OK", color="#888888", size=12) if error else ft.Container()
            ], spacing=2)
        ], spacing=10)
        
        test_results.controls.append(result_row)
        page.update()
    
    def run_all_tests(e):
        """Ejecuta todos los tests"""
        test_results.controls.clear()
        status_text.value = "Ejecutando tests..."
        status_text.color = "orange"
        page.update()
        
        # Test 1: Text básico
        def test_text():
            t = ft.Text("Test", color="white")
        
        passed = runner.run_test("Text Control", test_text)
        add_result("Text Control", passed, runner.results["tests"]["Text Control"].get("error"))
        
        # Test 2: Container
        def test_container():
            c = ft.Container(content=ft.Text("Test"), bgcolor="#111111", padding=10)
        
        passed = runner.run_test("Container", test_container)
        add_result("Container", passed, runner.results["tests"]["Container"].get("error"))
        
        # Test 3: Column/Row
        def test_layout():
            col = ft.Column([ft.Text("1"), ft.Text("2")])
            row = ft.Row([ft.Text("A"), ft.Text("B")])
        
        passed = runner.run_test("Column/Row Layout", test_layout)
        add_result("Column/Row Layout", passed, runner.results["tests"]["Column/Row Layout"].get("error"))
        
        # Test 4: TextField
        def test_textfield():
            tf = ft.TextField(hint_text="Test", color="white")
        
        passed = runner.run_test("TextField", test_textfield)
        add_result("TextField", passed, runner.results["tests"]["TextField"].get("error"))
        
        # Test 5: IconButton
        def test_iconbutton():
            btn = ft.IconButton(icon="send", icon_color="white")
        
        passed = runner.run_test("IconButton", test_iconbutton)
        add_result("IconButton", passed, runner.results["tests"]["IconButton"].get("error"))
        
        # Test 6: BoxConstraints (puede fallar)
        def test_boxconstraints():
            c = ft.Container(
                content=ft.Text("Test"),
                constraints=ft.BoxConstraints(max_width=100)
            )
        
        passed = runner.run_test("BoxConstraints", test_boxconstraints)
        add_result("BoxConstraints (Optional)", passed, runner.results["tests"]["BoxConstraints"].get("error"))
        
        # Test 7: ft.icons enum (puede fallar)
        def test_icons_enum():
            i = ft.Icon(ft.icons.SEND)
        
        passed = runner.run_test("ft.icons enum", test_icons_enum)
        add_result("ft.icons enum (Optional)", passed, runner.results["tests"]["ft.icons enum"].get("error"))
        
        # Resumen
        total = len(runner.results["tests"])
        passed_count = sum(1 for t in runner.results["tests"].values() if t["status"] == "PASS")
        
        status_text.value = f"Tests completados: {passed_count}/{total} pasaron"
        status_text.color = "green" if passed_count == total else "orange"
        page.update()
    
    # Layout
    page.add(
        ft.Column([
            ft.Row([
                ft.Icon("science", color="#00f2ff", size=30),
                ft.Text("COMPATIBILITY TESTER", size=24, weight="bold", color="#00f2ff")
            ], spacing=10),
            
            ft.Divider(color="white24"),
            
            version_text,
            
            ft.Container(height=20),
            
            ft.Container(
                content=test_results,
                border=ft.border.all(1, "white24"),
                border_radius=10,
                padding=15,
                expand=True
            ),
            
            ft.Container(height=10),
            
            status_text,
            
            ft.Container(height=10),
            
            ft.Row([
                ft.ElevatedButton(
                    "EJECUTAR TESTS",
                    on_click=run_all_tests,
                    bgcolor="#00f2ff",
                    color="black",
                    width=200
                ),
                ft.TextButton(
                    "Cerrar",
                    on_click=lambda e: page.window_close(),
                    style=ft.ButtonStyle(color="white")
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], expand=True, spacing=10)
    )

if __name__ == "__main__":
    print("Iniciando Flet Compatibility Tester...")
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona ENTER para salir...")
