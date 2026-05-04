from pathlib import Path
import os

# Definimos la ruta base del proyecto usando pathlib (más moderno y limpio que os.path)
BASE_DIR = Path(__file__).resolve().parent

# Definimos las rutas de carpetas
EVIDENCIA_DIR = BASE_DIR / "reports" / "evidencias"

# Configuración del Navegador
BROWSER = "edge"  # Opciones: "edge", "chrome", "firefox"
HEADLESS = False  # Cambiar a True para ejecuciones en CI/CD o segundo plano
IMPLICIT_WAIT = 10

# Crear directorios necesarios
EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)