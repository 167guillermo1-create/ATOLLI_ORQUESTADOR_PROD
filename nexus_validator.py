import ast
import os
import sys

def check_syntax(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        ast.parse(content)
        return True, "OK"
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"

def check_self_scope(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    
    errors = []
    class NameVisitor(ast.NodeVisitor):
        def __init__(self):
            self.in_class = False

        def visit_ClassDef(self, node):
            old_state = self.in_class
            self.in_class = True
            self.generic_visit(node)
            self.in_class = old_state

        def visit_Name(self, node):
            if node.id == 'self' and not self.in_class:
                errors.append(f"Invalid 'self' at line {node.lineno}")
            self.generic_visit(node)

    NameVisitor().visit(tree)
    return errors

def main():
    files_to_check = ['main.py']
    brain_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brain')
    
    if os.path.exists(brain_dir):
        for f in os.listdir(brain_dir):
            if f.endswith('.py'):
                files_to_check.append(os.path.join(brain_dir, f))

    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexus_validation_report.txt")
    
    with open(report_path, "w", encoding="utf-8") as report_file:
        def log(msg):
            print(msg)
            report_file.write(msg + "\n")

        log("--- ATOLLI NEXUS INTEGRITY SCAN ---")
        all_ok = True
        for f in files_to_check:
            full_path = f if os.path.isabs(f) else os.path.abspath(f)
            
            if not os.path.exists(full_path): 
                log(f"[MISSING] {full_path}")
                continue
                
            ok, msg = check_syntax(full_path)
            if ok:
                log(f"[SYNTAX OK] {os.path.basename(full_path)}")
                if os.path.basename(full_path) == 'main.py' or 'brain' in full_path:
                    self_errors = check_self_scope(full_path)
                    if self_errors:
                        log(f"  [SCOPE ERR] {os.path.basename(full_path)}: {self_errors}")
                        all_ok = False
                    else:
                        log(f"  [SCOPE OK] {os.path.basename(full_path)}")
            else:
                log(f"[SYNTAX ERR] {os.path.basename(full_path)}: {msg}")
                all_ok = False

        if all_ok:
            log("\n✅ SYSTEM INTEGRITY VERIFIED: PHOENIX IS READY.")
        else:
            log("\n❌ INTEGRITY CRITICAL: ERRORS DETECTED.")

if __name__ == "__main__":
    main()
