import os
from pathlib import Path

# Definición de la ruta base del proyecto usando pathlib (multiplataforma y robusto)
BASE_DIR = Path(__file__).resolve().parent

# --- DIRECTORIOS DEL FRAMEWORK ---
REPORTS_DIR = BASE_DIR / "reports"
EVIDENCIA_DIR = REPORTS_DIR / "evidencias"

# --- CONFIGURACIÓN DEL NAVEGADOR ---
# Permitimos sobrescribir la configuración mediante variables de entorno (Ideal para CI/CD)
BROWSER = os.getenv("QA_BROWSER", "edge")  # Opciones: "edge", "chrome", "firefox"

# Configuramos Headless en True por defecto para ejecuciones paralelas limpias y estables
# (Se puede forzar a False desde la terminal si alguna vez necesitas ver la interfaz visual)
env_headless = os.getenv("HEADLESS", "True")
HEADLESS = env_headless.lower() in ("true", "1", "t", "yes")

# --- TIMEOUTS GLOBALES ---
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15

# --- INICIALIZACIÓN DE DIRECTORIOS ---
# Garantiza que la estructura de reportes y evidencias exista antes de iniciar las pruebas
EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)