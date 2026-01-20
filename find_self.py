import ast
import os

def check_file(filepath):
    print(f"Checking {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    class SelfFinder(ast.NodeVisitor):
        def __init__(self):
            self.in_class = False

        def visit_ClassDef(self, node):
            old_in_class = self.in_class
            self.in_class = True
            self.generic_visit(node)
            self.in_class = old_in_class

        def visit_Name(self, node):
            if node.id == "self" and not self.in_class:
                print(f"❌ FOUND 'self' outside class! Line {node.lineno}")
            self.generic_visit(node)

    finder = SelfFinder()
    finder.visit(tree)

check_file("main.py")
for f in os.listdir("brain"):
    if f.endswith(".py"):
        check_file(os.path.join("brain", f))
