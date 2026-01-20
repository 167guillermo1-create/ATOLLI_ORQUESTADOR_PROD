# 🏁 PUNTO DE CONTROL DE ESTABILIDAD (ENERO 2026)
**ESTADO**: 🟢 ESTABLE Y OPERATIVO
**FECHA**: 2026-01-18
**HASH**: `FLET0802-CK-PY311`

---

## 🛑 ¡ALTO! LEER ANTES DE TOCAR NADA
Este documento certifica que el sistema funcionó perfectamente bajo las siguientes condiciones estrictas. **Cualquier desviación de esta configuración se considera SABOTAJE.**

### 1. LA TRINIDAD DE LA ESTABILIDAD
Para que la interfaz gráfica (GUI) arranque y sea visible, se requieren estos 3 pilares inamovibles:

| Componente | Versión/Valor EXACTO | ¿Por qué? |
| :--- | :--- | :--- |
| **Python** | `3.11.x` | Versiones más nuevas rompen Flet en ciertos OS. |
| **Flet** | `0.80.2` | Versiones anteriores no tienen features necesarios. Versiones futuras rompen APIs. |
| **Renderer** | `CANVAS_KIT` | `HTML` renderer FUE ELIMINADO. Usarlo causa CRASH inmediato. |

### 2. POST-MORTEM: EL ERROR "CRASH HTML"
**El Incidente:** El 18 de Enero de 2026, el sistema colapsó al intentar iniciar el modo Web (Oculus).
**La Causa:** Un script antiguo (`debug_web_launcher.py`) intentaba forzar `web_renderer=ft.WebRenderer.HTML`.
**El Hecho:** En Flet 0.80.2, `ft.WebRenderer.HTML` **NO EXISTE**.
**La Solución:** Se migró forzosamente a `ft.WebRenderer.CANVAS_KIT`.

**🚨 REGLA DE ORO:** NUNCA escribas código que especifique `renderer="html"`.

### 3. DIRECTIVAS DE INICIO DE SESIÓN (CÓMO NO ROMPERLO)
Si eres una IA retomando este proyecto, **NO EMPIECES DE CERO**. Sigue estos pasos:

1.  **NO TOQUES `requirements.txt`**: Ya está fijado en `flet==0.80.2`. No lo cambies a `latest` o `>=`.
2.  **SI VAS A VALIDAR**: Usa `diagnose_crash.py` o `diagnose_flet.py` primero. No asumas que el entorno está roto solo porque sí.
3.  **SI EL USUARIO PIDE "VERIFICAR"**: Ejecuta la opción 2 del menú (`debug_web_launcher.py`). Si carga la pantalla negra con letras cian neon, **TODO ESTÁ BIEN**.
4.  **NO REINSTALES**: A menos que `pip show flet` diga algo diferente a 0.80.2.

### 4. COMPONENTES CERTIFICADOS
Los siguientes módulos han sido probados y funcionan visualmente:
*   [x] **Chat Brain**: Envía y recibe (simulado si no hay API Key).
*   [x] **Factory**: Cards con efecto "Liquid Glass" y "Bento".
*   [x] **Config**: Campos de texto con passwords ocultos.

---
**FIRMA DEL ARQUITECTO:**
*Estabilidad alcanzada tras corrección de Renderer. No retroceder.*
