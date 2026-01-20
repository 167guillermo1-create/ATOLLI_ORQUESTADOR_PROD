import flet as ft
print("ft.Animation:", hasattr(ft, "Animation"))
print("ft.animation:", hasattr(ft, "animation"))
try:
    print(ft.Animation)
except:
    print("No ft.Animation")
