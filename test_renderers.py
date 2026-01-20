import flet as ft
renderers = ["canvaskit", "skwasm", "html", "auto"]
results = {}
for r in renderers:
    try:
        # We don't need a target to test the argument validation
        ft.WebRenderer(r)
        results[r] = "VALID"
    except Exception as e:
        results[r] = f"INVALID: {e}"

with open("renderer_test.txt", "w") as f:
    import json
    json.dump(results, f, indent=4)
