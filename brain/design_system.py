import flet as ft

class DesignRegistry:
    """
    Registry of high-end UI design archetypes for Atolli Nexus.
    Maps design concepts to Flet-compatible token sets.
    """
    
    # AURORA GLASS PALETTE (2026 Luxury Standard)
    # Deep Space Void -> Cosmic Blue
    AURORA_GRADIENT_COLORS = ["#000428", "#004e92", "#050116"] 
    NEON_CYAN = "#00f2ff"
    NEON_PURPLE = "#bc13fe"
    GLASS_BORDER = "#ffffff22" # Low opacity white
    GLASS_BG = "#0f172a80" # Dark slate with 50% opacity
    
    ARCHETYPES = {
        "aurora_glass": {
            "name": "Aurora Glass 2026",
            "description": "Vibrant gradients with deep frosted glass effects.",
            "gradient_bg": ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=["#000428", "#004e92"],
            ),
            "accent": NEON_CYAN,
            "text_color": "#e2e8f0",
            "glass_bgcolor": "#1e293b4d", # ~30% opacity slate
            "blur": 20,
            "border_radius": 16,
            "border_color": "#ffffff1a"
        }
    }

    @classmethod
    def get_main_background(cls):
        """Returns the signature Aurora LinearGradient."""
        return ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=cls.AURORA_GRADIENT_COLORS,
            tile_mode=ft.GradientTileMode.MIRROR
        )

    @classmethod
    def get_glass_card(cls, content, width=None, height=None, padding=20, expand=False, **kwargs):
        """Generates a premium Glassmorphic container."""
        tokens = cls.ARCHETYPES["aurora_glass"]
        return ft.Container(
            content=content,
            width=width,
            height=height,
            padding=padding,
            expand=expand,
            bgcolor=tokens["glass_bgcolor"],
            blur=tokens["blur"],
            border=ft.border.all(1, tokens["border_color"]),
            border_radius=tokens["border_radius"],
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#00000040",
                offset=ft.Offset(0, 4),
            ),
            animate=ft.Animation(400, ft.AnimationCurve.DECELERATE),
            **kwargs
        )

    @classmethod
    def get_neon_button(cls, text, icon_name, on_click, selected=False):
        """Generates a neon-accented navigation button."""
        tokens = cls.ARCHETYPES["aurora_glass"]
        
        # Color logic: filled if selected, transparent/ghost if not
        bg_color = tokens["accent"] if selected else "#00000000"
        content_color = "#000000" if selected else tokens["accent"]
        elevation = 10 if selected else 0
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon_name, color=content_color, size=18),
                    ft.Text(text, color=content_color, weight=ft.FontWeight.BOLD if selected else ft.FontWeight.NORMAL, size=14)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8
            ),
            on_click=on_click,
            bgcolor=bg_color,
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            border_radius=12,
            border=ft.border.all(1, tokens["accent"]) if not selected else None,
            shadow=ft.BoxShadow(
                blur_radius=15, 
                color=tokens["accent"], 
            ) if selected else None,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            ink=True,
            # Use data attribute to store type for identifying later if needed
            data=text
        )

    @classmethod
    def get_header_label(cls, text):
        return ft.Text(
            text, 
            size=28, 
            weight=ft.FontWeight.W_900, 
            color="white",
            font_family="Roboto Mono"
        )

    @classmethod
    def get_token_code(cls, archetype="aurora_glass"):
        """Returns a string representation of tokens for injection into files."""
        tokens = cls.ARCHETYPES.get(archetype, cls.ARCHETYPES["aurora_glass"])
        return f"# Design Tokens for {tokens['name']}\nTOKENS = {tokens}\n"

class ResponsiveScanner:
    """
    Intelligence layer to detect device context and adapt layout.
    Chapter 3 - 'Responsive Row & Design'
    """
    MOBILE_BREAKPOINT = 600
    TABLET_BREAKPOINT = 1024
    
    @staticmethod
    def get_device_type(page_width):
        if page_width < ResponsiveScanner.MOBILE_BREAKPOINT:
            return "MOBILE"
        elif page_width < ResponsiveScanner.TABLET_BREAKPOINT:
            return "TABLET"
        else:
            return "DESKTOP"

    @staticmethod
    def get_column_count(page_width):
        """Returns optimal grid columns based on width."""
        dtype = ResponsiveScanner.get_device_type(page_width)
        if dtype == "MOBILE": return 1
        if dtype == "TABLET": return 2
        return 4 # Desktop standard

