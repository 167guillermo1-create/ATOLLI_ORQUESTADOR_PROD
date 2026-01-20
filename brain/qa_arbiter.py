import ast

class QAArbiter:
    """
    The Logic Guardian of Atolli Nexus.
    Inspects generated code for UI connections, logic errors, and reachability.
    """
    
    def audit_code_logic(self, code_str):
        """
        Performs static analysis on the code to detect common failure points.
        """
        reports = []
        try:
            tree = ast.parse(code_str)
        except SyntaxError as e:
            return {"success": False, "errors": [f"Error de sintaxis: {str(e)}"]}

        # 1. Verificar existencia de funciones on_click
        click_handlers = []
        defined_functions = set()
        
        for node in ast.walk(tree):
            # Buscar definiciones de funciones
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined_functions.add(node.name)
            
            # Buscar asignaciones de handlers (on_click=...)
            if isinstance(node, ast.keyword) and node.arg == "on_click":
                if isinstance(node.value, ast.Name):
                    click_handlers.append(node.value.id)
                elif isinstance(node.value, ast.Lambda):
                    # Lambda complex analysis (simplified for now)
                    pass

        for handler in click_handlers:
            if handler not in defined_functions:
                reports.append(f"🔌 Handler huérfano: '{handler}' no está definido.")

        # 2. Verificar imports críticos (Robust)
        has_flet = False
        forbidden_controls = ["IconButton"] # Known to cause issues in Web CanvasKit v0.80
        found_forbidden = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "flet": has_flet = True
            elif isinstance(node, ast.ImportFrom):
                if node.module == "flet": has_flet = True
            
            # Check for forbidden controls
            if isinstance(node, ast.Attribute):
                if node.attr in forbidden_controls:
                    found_forbidden.append(node.attr)
            # Check if accessed directly e.g. ft.IconButton
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in forbidden_controls:
                         found_forbidden.append(node.func.attr)

        if not has_flet:
            reports.append("⚠️ Importación faltante: 'flet' no detectado.")
            
        if found_forbidden:
            reports.append(f"⚠️ Control Inestable detectado: {list(set(found_forbidden))}. Usar Elevated/FilledButton para Web.")

        success = len(reports) == 0
        return {
            "success": success,
            "errors": reports,
            "score": 100 if success else max(0, 100 - len(reports) * 20)
        }
