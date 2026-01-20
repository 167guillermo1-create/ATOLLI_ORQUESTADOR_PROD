# 👁️ PROTOCOLO NEXUS OCULUS (VERIFICACIÓN VISUAL)
## (AI AUTONOMOUS VISUAL VERIFICATION SYSTEM)

> **ESTADO**: OPERACIONAL / CRÍTICO
> **VERIFICACIÓN HISTÓRICA**: 2026-01-17 - Éxito total en restauración de UI.
> **REQUERIDO PARA**: Cualquier cambio que afecte la interfaz gráfica (UI).

### 1. OBJETIVO
Permitir que la Inteligencia Artificial (Tú) verifique autónomamente que la interfaz gráfica de Flet se está renderizando correctamente sin necesidad de pedir capturas de pantalla al usuario.

### 2. HERRAMIENTAS
Este protocolo utiliza un script lanzador específico y un Agente de Navegación (Browser Tool).

*   **Lanzador**: `debug_web_launcher.py`
*   **Puerto**: `8550` (localhost)
*   **Renderer**: `CANVAS_KIT` (Optimizado para compatibilidad)
*   **Entorno**: Python 3.11 (Requerido para estabilidad de Flet)

### 3. PROCEDIMIENTO (PASO A PASO)

#### FASE A: INICIO DEL SERVIDOR
Antes de intentar "ver" la app, debes iniciarla en modo servidor.

1.  **Ejecutar comando**:
    ```bash
    py -3.11 debug_web_launcher.py
    ```
    *(Nota: Si el puerto 8550 está ocupado o hay errores de Python, busca logs en la terminal).*

2.  **Esperar**: Dale unos 5-10 segundos para iniciar.

#### FASE B: INSPECCIÓN VISUAL (AGENT BROWSER)
Usa tu herramienta de navegador (`open_browser_url`, `click_browser_pixel`, etc.) para interactuar como humano.

1.  **Navegar**: Ve a `http://localhost:8550`.
2.  **Verificar Carga**: Busca el título "NEXUS MASTER GEN" o elementos clave.
3.  **Inspección Profunda**:
    *   Flet usa `<canvas>` para dibujar. Las herramientas de DOM estándar (`get_dom`) NO verán botones HTML "reales" dentro del canvas.
    *   **ESTRATEGIA**: Confía en la **interacción visual**.
    *   Usa `click_browser_pixel` si conoces las coordenadas aproximadas.
    *   Si el navegador soporta CanvasKit correctamente, deberías ser capaz de "ver" los cambios de estado (navegación entre pestañas).

#### FASE C: HANDOFF (ENTREGA AL HUMANO)
Si la verificación es exitosa:

1.  **NO MATE EL PROCESO**.
2.  Deje el servidor corriendo en el puerto 8550.
3.  Informe al usuario: "Prueba visual completada. Puedes revisar el resultado aquí: http://localhost:8550".
4.  Solo cierre el proceso si el usuario explícitamente pide "apagar el servidor" o al iniciar una nueva sesión de código intenso.

### 4. SOLUCIÓN DE PROBLEMAS COMUNES

| Síntoma | Causa Probable | Solución |
| :--- | :--- | :--- |
| Pantalla Azul/Blanca Vacía | WebGL no soportado por el Agente | Asegúrate de que `debug_web_launcher.py` use `ft.WebRenderer.CANVAS_KIT` o `HTML` (si es viable). |
| "Module not found" | Entorno incorrecto | Usa siempre `py -3.11` o verifica `.venv`. |
| No responde al click | Coordenadas erróneas | Calcula coordenadas basándote en un screenshot previo o en diseño estándar (Header ~100px alto). |

### 5. IMPLEMENTACIÓN EN CÓDIGO (REFERENCIA)
El archivo `debug_web_launcher.py` debe permanecer intacto con esta configuración:

```python
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, web_renderer=ft.WebRenderer.CANVAS_KIT)
```

### 6. PROTOCOLO DE ESCRITORIO (NEXUS OCULUS DESKTOP)
> **ESTADO**: BETA
> **REQUERIDO PARA**: Verificación de builds nativos y ventanas emergentes.

#### HERRAMIENTAS
*   **Launcher**: `debug_desktop_launcher.py`
*   **Librerías**: `pyautogui`, `mss`, `pygetwindow`, `opencv-python`

#### PROCEDIMIENTO
1.  **Iniciar**: Ejecutar `python debug_desktop_launcher.py`
2.  **Operación**:
    *   El script lanzará la app principal (`main.py`) en un subproceso.
    *   NexusOculus buscará la ventana "NEXUS MASTER GEN".
    *   Si la encuentra, tomará una captura (`verification_results/launch_view.png`).
    *   Analizará la integridad visual (detectará si es una pantalla negra/blanca).
    *   Cerrará la app automáticamente tras el test.
3.  **Verificación**:
    *   Revisar la salida de terminal: `🟢 Visual Integrity Check: PASS`
    *   Inspeccionar la imagen generada en `verification_results`.

