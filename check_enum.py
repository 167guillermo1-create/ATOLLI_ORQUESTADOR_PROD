import flet as ft
with open("enum_results.txt", "w") as f:
    f.write("WebRenderer Members:\n")
    try:
        for m in ft.WebRenderer:
            f.write(f" - {m.name}: {m.value}\n")
    except Exception as e:
        f.write(f"Error iterating: {e}\n")

    f.write("\ndir(WebRenderer):\n")
    f.write(str(dir(ft.WebRenderer)))
