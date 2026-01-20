# CONTROLES VERIFICADOS - REFERENCIA RÁPIDA

## ✅ SEGUROS (Verificados 2026-01-16)
- `ft.Text(value, color, size, weight, font_family)`
- `ft.Container(content, bgcolor, padding, border_radius, border, height)`
- `ft.Column(controls, spacing, scroll, height)`
- `ft.Row(controls, alignment, spacing)`
- `ft.TextField(hint_text, color, border_color, text_style, on_submit, width)`
- `ft.ElevatedButton(text, bgcolor, color, on_click)` ✅ Usar en lugar de IconButton
- `ft.Divider(color)`

## ❌ NO FUNCIONAN
- `ft.IconButton` - Error: "must have icon or visible content"

## ❌ EVITAR
- `expand=True` anidado
- Clases heredando de `ft.Container`
- `async def main` con bootloaders
- `page.clean()` repetido
- `ft.icons.CONSTANT` (usar strings)
- `ft.BoxConstraints`

## 📐 PATRÓN SEGURO
```python
page.add(control)
page.update()
```

Usar altura/ancho fijo en lugar de `expand=True`
