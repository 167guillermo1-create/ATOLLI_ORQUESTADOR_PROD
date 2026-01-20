# PROTOCOLO DE COMPATIBILIDAD FLET (GOLDEN FLET PROTOCOL)

> **📋 REFERENCIA RÁPIDA:** Ver `VERIFIED_CONTROLS.md` para lista completa de controles verificados en este sistema.

## REGLA DE ORO
**NUNCA uses una característica de Flet sin verificar que funciona en la versión instalada del usuario.**
**NUNCA uses `ft.WebRenderer.HTML` (Deprecado en 0.80.2+). Usa `CANVAS_KIT`.**

## PASO 1: DETECCIÓN DE VERSIÓN (OBLIGATORIO)
Antes de escribir CUALQUIER código Flet, ejecuta:
```python
python -c "import flet; print(flet.__version__)"
```
O crea un script de diagnóstico que lo haga automáticamente.

## PASO 2: LISTA BLANCA DE CARACTERÍSTICAS SEGURAS
Estas características funcionan en TODAS las versiones de Flet (0.1.x - 0.80.x+):

### Controles Básicos (SIEMPRE SEGUROS)
- `ft.Text(value, color="...", size=N)`
- `ft.Container(content=..., bgcolor="...", padding=N, border_radius=N)`
- `ft.Column(controls=[...], expand=True/False, spacing=N)`
- `ft.Row(controls=[...], alignment=ft.MainAxisAlignment.XXX)`
- `ft.TextField(hint_text="...", value="...", on_submit=func, color="...")`
- `ft.IconButton(icon="string_name", on_click=func, icon_color="...")`
- `ft.Divider(color="...")`
- `ft.Icon("string_name", color="...", size=N)` (usar strings, NO ft.icons.CONSTANT)

### Propiedades de Page (SIEMPRE SEGURAS)
- `page.title = "..."`
- `page.bgcolor = "#RRGGBB"`
- `page.padding = N`
- `page.window_width = N`
- `page.window_height = N`
- `page.theme_mode = ft.ThemeMode.DARK`
- `page.add(...)`
- `page.update()`

### Colores (SIEMPRE SEGUROS)
- Usar strings hexadecimales: `"#00f2ff"`, `"#050505"`
- Usar nombres básicos: `"white"`, `"black"`, `"green"`, `"red"`
- **EVITAR:** `ft.colors.BLUE_400` (puede no existir en versiones antiguas)

### Iconos (SIEMPRE SEGUROS)
- Usar strings: `icon="send"`, `icon="circle"`, `icon="settings"`
- **EVITAR:** `ft.icons.SEND` (puede no existir en versiones antiguas)

## PASO 3: LISTA NEGRA (CARACTERÍSTICAS PELIGROSAS)
Estas características pueden NO funcionar en todas las versiones:

### ❌ EVITAR (a menos que se verifique primero)
- `ft.BoxConstraints(max_width=...)` - No soportado en versiones <0.21
- `ft.alignment.center` - Usar `ft.Alignment(0,0)` en su lugar
- `ft.icons.CONSTANT` - Usar strings en su lugar
- `ft.colors.CONSTANT` - Usar hex strings en su lugar
- `async def main(page)` - Puede causar problemas de renderizado
- Clases heredando de `ft.Container` - Conflictos con propiedades internas
- `page.clean()` en loops - Puede causar pantallas grises
- **CRÍTICO**: `ft.WebRenderer.HTML` - CAUSA CRASH INMEDIATO. Eliminado en v0.80.2.

## PASO 4: PROTOCOLO DE PRUEBA INCREMENTAL

### Test Level 0: Ventana Vacía
```python
def main(page: ft.Page):
    page.title = "TEST"
    page.bgcolor = "black"
    page.update()
    page.add(ft.Text("FUNCIONA", color="green", size=30))
    page.update()
```
**Si esto falla:** Problema de instalación de Flet.

### Test Level 1: Layout Básico
```python
def main(page: ft.Page):
    page.title = "TEST"
    page.bgcolor = "black"
    page.update()
    
    layout = ft.Column([
        ft.Text("Header", color="white"),
        ft.Divider(color="white24"),
        ft.Container(content=ft.Text("Body"), expand=True),
        ft.Row([ft.TextField(hint_text="Input"), ft.IconButton(icon="send")])
    ], expand=True)
    
    page.add(layout)
    page.update()
```
**Si esto falla:** Problema con layouts complejos.

### Test Level 2: Interactividad
```python
def main(page: ft.Page):
    page.title = "TEST"
    page.bgcolor = "black"
    page.update()
    
    output = ft.Text("", color="white")
    
    def click(e):
        output.value = "CLICKED"
        page.update()
    
    page.add(ft.Column([
        output,
        ft.IconButton(icon="send", on_click=click)
    ]))
    page.update()
```
**Si esto falla:** Problema con event handlers.

## PASO 5: REGLAS DE CONSTRUCCIÓN

### ✅ HACER
1. Usar funciones simples, no clases complejas
2. Llamar `page.update()` después de cambios
3. Usar strings para iconos y colores
4. Probar cada nivel antes de avanzar
5. Mantener layouts simples (Column/Row directos)

### ❌ NO HACER
1. Asumir que una característica existe sin probar
2. Usar `async` a menos que sea absolutamente necesario
3. Heredar de controles de Flet (`ft.Container`, etc.)
4. Usar constantes de enums sin verificar
5. Hacer `page.clean()` repetidamente

## PASO 6: SCRIPT DE VALIDACIÓN AUTOMÁTICA

Crear `flet_validator.py` que:
1. Detecta versión de Flet
2. Ejecuta Tests Level 0, 1, 2
3. Genera reporte de compatibilidad
4. Crea lista de características verificadas

## RESUMEN EJECUTIVO

**Antes de escribir código:**
1. ✅ Detectar versión de Flet
2. ✅ Usar solo características de Lista Blanca
3. ✅ Probar con Test Level 0
4. ✅ Construir incrementalmente (Level 1, 2, etc.)
5. ✅ Si algo falla, retroceder al último nivel que funcionó

**Mantra:** "Si no lo probé, no existe."
