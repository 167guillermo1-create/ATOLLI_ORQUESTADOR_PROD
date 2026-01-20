# NEXUS MASTER GEN - MANUAL DE OPERACIONES 🚀

Bienvenido al núcleo de mando de Atolli. Este documento detalla cómo operar, compilar y expandir el ecosistema Nexus Master Gen.

## 1. Modos de Ejecución 🖥️

### Modo Web (Desarrollo y Demo)
Ideal para prototipado rápido y acceso remoto.
- **Comando**: `flet run --web main.py`
- **Url**: `http://localhost:8550` (o el puerto que asigne Flet).

### Modo Desktop (Nativo)
Para una experiencia de usuario premium con Aurora Glass UI a máxima fluidez.
- **Comando**: `python main.py`

---

## 2. Compilación y Distribución 📦

### Generar Ejecutable Windows (.EXE)
Nexus incluye un script de automatización que gestiona los assets e iconos.
- **Comando**: `python build_production.py`
- **Resultado**: El binario estará en `dist/windows/Nexus Master Gen.exe`.
- **Nota**: Asegúrate de que `assets/icon.png` esté presente.

### Generar Android APK (.APK)
Hemos automatizado esto mediante CI/CD en la nube para asegurar una compilación limpia.
- **Acción**: Sube el código a tu repositorio de GitHub.
- **Automatización**: Revisa la pestaña **Actions** en GitHub. Una vez termine el workflow "Build Android APK", podrás descargar el archivo directamente desde los artefactos del job.

---

## 3. Comandos de Consola Nexus 🧠

Desde el chat del orquestador puedes usar los siguientes triggers tácticos:

| Comando | Acción | Propósito |
| :--- | :--- | :--- |
| `/status` | Monitor de Motores | Verifica qué LLMs están conectados y operativos. |
| `/evolve` | Síntesis Cognitiva | Muestra tu Rango, XP, Medallas y un resumen de la sesión. |
| `/help` | Guía Rápida | Muestra la lista de comandos disponibles. |
| `test_break` | Auditoría de Inmunidad | Simula un fallo de importación para verificar el Auto-Healing. |

---

## 4. Arquitectura Full-Stack 🛠️

Para crear un nuevo proyecto controlado por Nexus:
1. Pide a Nexus: "Crear un proyecto full stack llamado [Nombre] con tabla de [Entidad]".
2. Nexus usará el **FactoryManager** para:
   - Crear la estructura local de archivos.
   - Aprovisionar la base de datos en **Supabase** (vía RPC).
   - Inyectar el código inicial verificado.

---

## 5. Mantenimiento de la IA (The Brain) 🧬

- **Configuración**: El archivo `data/.env` centraliza tus API Keys (Groq, Gemini, OpenAI, Supabase).
- **Evolución**: El estado se guarda automáticamente en `nexus_state.json` y se sincroniza con Supabase Cloud.
- **Auto-Healing**: Si el sistema detecta un `ImportError`, intentará ejecutar un `pip install` del paquete faltante de forma autónoma.

**Nexus Master Gen está ahora en nivel Nexus-Ascendant. ¡Buen trabajo, Arquitecto!** 📐✨
