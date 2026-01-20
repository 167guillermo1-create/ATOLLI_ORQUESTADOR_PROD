import flet as ft
from brain.design_system import DesignRegistry

class LuxuryStepper(ft.Row):
    """
    A glassmorphic progress indicator for multi-step workflows.
    Chapter 3 - 'Interfaces de Configuración Simplificadas'
    """
    def __init__(self, current_step, total_steps, **kwargs):
        super().__init__(**kwargs)
        self.current_step = current_step
        self.total_steps = total_steps
        self.tokens = DesignRegistry.ARCHETYPES["aurora_glass"]
        self.spacing = 8
        self.alignment = ft.MainAxisAlignment.CENTER
        
        # Build controls immediately
        steps = []
        for i in range(1, self.total_steps + 1):
            is_active = i <= self.current_step
            is_current = i == self.current_step
            
            steps.append(
                ft.Container(
                    width=40 if is_current else 12,
                    height=12,
                    border_radius=6,
                    bgcolor=self.tokens["accent"] if is_active else "#ffffff20",
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
                    shadow=ft.BoxShadow(blur_radius=10, color=self.tokens["accent"]) if is_current else None
                )
            )
        self.controls = steps

class GlassInput(ft.Container):
    """
    Premium input field with floating effect and focus glow.
    """
    def __init__(self, hint_text, on_submit=None, password=False, icon=None, **kwargs):
        super().__init__(**kwargs)
        self.tokens = DesignRegistry.ARCHETYPES["aurora_glass"]
        
        # Inner text field
        self.input_field = ft.TextField(
            hint_text=hint_text,
            password=password,
            color=self.tokens["text_color"],
            border=ft.InputBorder.NONE,
            bgcolor="transparent",
            on_submit=on_submit,
            text_style=ft.TextStyle(size=14, font_family="Verdana"),
            cursor_color=self.tokens["accent"],
            content_padding=15
        )

        # Container styling (Aurora Glass)
        self.bgcolor = self.tokens["glass_bgcolor"]
        self.blur = self.tokens["blur"]
        self.border = ft.Border.all(1, self.tokens["border_color"])
        self.border_radius = self.tokens["border_radius"]
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color="#00000040",
            offset=ft.Offset(0, 4),
        )
        self.animate = ft.Animation(400, ft.AnimationCurve.DECELERATE)
        self.padding = 0
        self.height = 50
        
        # Content
        self.content = ft.Row([
            ft.Icon(icon, color=self.tokens["accent"], size=20) if icon else ft.Container(),
            ft.Container(content=self.input_field, expand=True)
        ], alignment=ft.MainAxisAlignment.START, spacing=10)

class SmartTooltip(ft.Tooltip):
    """
    AI-powered tooltip placeholder. 
    In future, this will connect to RAG for explanations.
    """
    def __init__(self, message, **kwargs):
        super().__init__(message=message, **kwargs)
        self.message = message
        self.content = ft.Icon("info_outline", color="#ffffff80", size=16)
        self.padding = 10
        self.border_radius = 8
        self.bgcolor = "#0f172a"
        self.text_style = ft.TextStyle(color="white", size=12)
