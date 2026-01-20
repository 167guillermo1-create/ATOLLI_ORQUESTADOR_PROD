import flet as ft
import os
import json

def main(page: ft.Page):
    page.title = "Atolli Fusion Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 800
    page.window_height = 600
    page.padding = 30

    def get_projects():
        projects = []
        factory_path = os.path.join(os.getcwd(), "Factory")
        if os.path.exists(factory_path):
            for item in os.listdir(factory_path):
                path = os.path.join(factory_path, item)
                if os.path.isdir(path):
                     # Check for manifest
                     manifest_path = os.path.join(path, "nexus_manifest.json")
                     details = "No manifest (Legacy)"
                     lineage_badge = None
                     
                     if os.path.exists(manifest_path):
                         try:
                             with open(manifest_path, "r") as f:
                                 data = json.load(f)
                                 details = f"v{data.get('version')} • {data.get('backend')}"
                                 if "lineage" in data:
                                     lineage_badge = ft.Container(
                                         content=ft.Text(data['lineage'], size=10, color="white"),
                                         bgcolor="blue", padding=5, border_radius=5
                                     )
                         except:
                             pass
                     
                     trailing = lineage_badge if lineage_badge else ft.Icon(ft.icons.HISTORY, color="grey")
                     
                     projects.append(ft.ListTile(
                         title=ft.Text(item, weight="bold", size=16),
                         subtitle=ft.Text(details, color="grey"),
                         leading=ft.Icon(ft.icons.FOLDER, color="amber"),
                         trailing=trailing
                     ))
        return projects

    def get_knowledge_status():
        kb_path = os.path.join(os.getcwd(), "knowledge_base")
        if not os.path.exists(kb_path):
            return ft.Text("❌ Knowledge Base no encontrada", color="red")
        
        files = os.listdir(kb_path)
        return ft.Column([
            ft.Text(f"✅ Base de Conocimiento Activa ({len(files)} protocolos)", color="green", weight="bold"),
            ft.Text("• Golden Protocol: ACTIVO", size=12, color="green"),
            ft.Text("• Flet Compatibility: ACTIVO", size=12, color="green"),
            ft.Text("• Master Roadmap: ACTIVO", size=12, color="green")
        ])

    page.add(
        ft.Text("Atolli Nexus: Fusion Dashboard", size=30, weight="bold", font_family="Segoe UI"),
        ft.Divider(),
        get_knowledge_status(),
        ft.Container(height=20),
        ft.Text("Proyectos en Factory", size=20, weight="bold"),
        ft.Text("Lista unificada de instancias detectadas", size=12, color="grey"),
        ft.Container(height=10),
        ft.Container(
            content=ft.ListView(controls=get_projects(), expand=True, spacing=10),
            border=ft.border.all(1, "white10"),
            border_radius=10,
            padding=10,
            height=300
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
