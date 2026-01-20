import sys
print("Inicio Test Simple")
try:
    import groq
    print("Groq importado correctamente")
except ImportError as e:
    print(f"Error importando groq: {e}")

try:
    import flet
    print("Flet importado correctamente")
except ImportError as e:
    print(f"Error importando flet: {e}")
print("Fin Test Simple")
