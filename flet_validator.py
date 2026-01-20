"""
FLET COMPATIBILITY VALIDATOR
Verifica que características de Flet funcionan en este sistema.
"""
import flet as ft
import sys

# Resultados
results = {
    "version": None,
    "level_0": False,
    "level_1": False,
    "level_2": False,
    "features": {}
}

def test_level_0():
    """Test básico: Ventana + Texto"""
    try:
        def main(page: ft.Page):
            page.title = "LEVEL 0 TEST"
            page.bgcolor = "black"
            page.update()
            page.add(ft.Text("LEVEL 0 OK", color="green", size=20))
            page.update()
            results["level_0"] = True
        
        ft.app(target=main)
        return True
    except Exception as e:
        print(f"LEVEL 0 FAILED: {e}")
        return False

def test_level_1():
    """Test de Layout: Column/Row/Container"""
    try:
        def main(page: ft.Page):
            page.title = "LEVEL 1 TEST"
            page.bgcolor = "black"
            page.update()
            
            layout = ft.Column([
                ft.Text("Header", color="white"),
                ft.Divider(color="white24"),
                ft.Container(
                    content=ft.Text("Body", color="white"),
                    bgcolor="#111111",
                    padding=10,
                    expand=True
                ),
                ft.Row([
                    ft.TextField(hint_text="Input", color="white"),
                    ft.IconButton(icon="send", icon_color="white")
                ])
            ], expand=True)
            
            page.add(layout)
            page.update()
            results["level_1"] = True
        
        ft.app(target=main)
        return True
    except Exception as e:
        print(f"LEVEL 1 FAILED: {e}")
        return False

def test_level_2():
    """Test de Interactividad: Eventos"""
    try:
        def main(page: ft.Page):
            page.title = "LEVEL 2 TEST"
            page.bgcolor = "black"
            page.update()
            
            output = ft.Text("Click the button", color="white")
            
            def click(e):
                output.value = "LEVEL 2 OK"
                page.update()
                results["level_2"] = True
            
            page.add(ft.Column([
                output,
                ft.IconButton(icon="send", on_click=click, icon_color="green")
            ]))
            page.update()
        
        ft.app(target=main)
        return True
    except Exception as e:
        print(f"LEVEL 2 FAILED: {e}")
        return False

def test_feature_boxconstraints():
    """Test BoxConstraints"""
    try:
        def main(page: ft.Page):
            page.bgcolor = "black"
            page.add(ft.Container(
                content=ft.Text("Test"),
                constraints=ft.BoxConstraints(max_width=100)
            ))
            page.update()
            results["features"]["BoxConstraints"] = True
        
        ft.app(target=main)
        return True
    except:
        results["features"]["BoxConstraints"] = False
        return False

def test_feature_icons_enum():
    """Test ft.icons.CONSTANT"""
    try:
        def main(page: ft.Page):
            page.bgcolor = "black"
            page.add(ft.Icon(ft.icons.SEND))
            page.update()
            results["features"]["icons_enum"] = True
        
        ft.app(target=main)
        return True
    except:
        results["features"]["icons_enum"] = False
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("FLET COMPATIBILITY VALIDATOR")
    print("=" * 50)
    
    # Detect version
    try:
        results["version"] = ft.__version__
        print(f"\n✓ Flet Version: {ft.__version__}")
    except:
        print("\n✗ Cannot detect Flet version")
        sys.exit(1)
    
    print("\nRunning tests...")
    print("(Close each window to proceed to next test)\n")
    
    # Run tests
    input("Press ENTER to start LEVEL 0 test (Basic Window)...")
    test_level_0()
    
    if results["level_0"]:
        print("✓ LEVEL 0: PASSED")
        input("\nPress ENTER to start LEVEL 1 test (Layouts)...")
        test_level_1()
        
        if results["level_1"]:
            print("✓ LEVEL 1: PASSED")
            input("\nPress ENTER to start LEVEL 2 test (Interactivity)...")
            test_level_2()
            
            if results["level_2"]:
                print("✓ LEVEL 2: PASSED")
    
    # Feature tests
    print("\n" + "=" * 50)
    print("FEATURE TESTS")
    print("=" * 50)
    
    input("\nPress ENTER to test BoxConstraints...")
    test_feature_boxconstraints()
    print(f"BoxConstraints: {'✓ SUPPORTED' if results['features'].get('BoxConstraints') else '✗ NOT SUPPORTED'}")
    
    input("\nPress ENTER to test ft.icons enum...")
    test_feature_icons_enum()
    print(f"ft.icons enum: {'✓ SUPPORTED' if results['features'].get('icons_enum') else '✗ NOT SUPPORTED'}")
    
    # Final report
    print("\n" + "=" * 50)
    print("FINAL REPORT")
    print("=" * 50)
    print(f"Flet Version: {results['version']}")
    print(f"Level 0 (Basic): {'✓ PASS' if results['level_0'] else '✗ FAIL'}")
    print(f"Level 1 (Layouts): {'✓ PASS' if results['level_1'] else '✗ FAIL'}")
    print(f"Level 2 (Events): {'✓ PASS' if results['level_2'] else '✗ FAIL'}")
    print("\nFeature Support:")
    for feature, supported in results['features'].items():
        print(f"  {feature}: {'✓' if supported else '✗'}")
    
    print("\n" + "=" * 50)
    if all([results['level_0'], results['level_1'], results['level_2']]):
        print("✓ ALL CORE TESTS PASSED - System is compatible")
    else:
        print("✗ SOME TESTS FAILED - Check compatibility")
    print("=" * 50)
