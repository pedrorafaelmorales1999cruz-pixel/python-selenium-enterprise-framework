# 🚀 QA Automation Framework - Selenium & Python

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Selenium](https://img.shields.io/badge/selenium-4.0%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Headless Mode](https://img.shields.io/badge/headless-supported-success)

Este repositorio contiene un **Framework de Automatización de Pruebas E2E** de nivel empresarial. Ha sido diseñado bajo estrictos principios de **Clean Code** y **Patrones de Diseño**, ofreciendo una solución altamente escalable, resiliente y lista para CI/CD para la validación de aplicaciones web.

---

## 🛡️ Aviso de Seguridad y Privacidad
Este framework ha sido diseñado con un enfoque de **Privacidad Total** y **Seguridad del Entorno**:
- **Ejecución 100% Local:** El código no realiza conexiones externas a servidores de terceros, no recolecta telemetría ni envía información de tu equipo a ninguna base de datos externa.
- **Cero Rastreo de Rutas:** Se utiliza la librería `pathlib` para que todas las operaciones de archivos sean relativas al proyecto. No se filtran nombres de usuario de Windows ni rutas absolutas en los reportes o logs.
- **Aislamiento de Datos:** El archivo `.gitignore` bloquea la subida accidental de capturas de pantalla, código fuente HTML de fallos y archivos de configuración personal.
- **Seguridad de Credenciales:** Preparado para utilizar variables de entorno (`os.getenv`) sin exponer datos sensibles en el código fuente.
- **Entornos Aislados:** Optimizado para ejecutarse dentro de entornos virtuales (`venv`) garantizando total limpieza en el sistema operativo.

---

## 🧠 Arquitectura: El "Wow Factor"
La pieza clave de este framework es su **Lógica de Introspección**. Mediante el uso de la librería `inspect`, la clase `BaseTest` identifica automáticamente qué script hijo la está invocando. Esto permite:
1. Organizar evidencias automáticamente por Carpeta/Proyecto/Script sin requerir configuración manual en cada prueba.
2. Detectar el contexto de ejecución (Manual vs. Orquestado mediante variables de sesión).
3. Inyectar y configurar el WebDriver de manera transparente y desacoplada.

---

## 🌟 Características Principales
- **Orquestador Quirúrgico (`run_tests.py`):** Motor inteligente con auto-descubrimiento mediante patrones `glob`, exclusión estricta de directorios del sistema/librerías externas, medición de tiempos y soporte para ejecución multi-hilo o secuencial.
- **Modo Headless Avanzado y Robusto:** Configurable desde `config.py` y optimizado en `BaseTest` con argumentos de estabilidad (`--window-size=1920,1080`, `--disable-gpu`, `--no-sandbox`) para simular un monitor de escritorio completo en segundo plano sin fallos por renderizado.
- **Gestión Jerárquica de Evidencias:** Sistema automatizado forense que organiza capturas de éxito y código fuente HTML (`.html`) por `ID de Sesión / Proyecto / Script`.
- **Persistencia de Reportes:** Generación automática de un log consolidado (`execution_summary.log`) al finalizar cada corrida de pruebas.

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.10+
- **Automatización:** Selenium WebDriver (Edge / Multi-navegador)
- **Concurrencia:** `concurrent.futures` (ProcessPoolExecutor)
- **Análisis Estático:** Pylance (Type Checking Mode: Strict/Basic)

## 📂 Estructura del Proyecto
```plaintext
PROYECTOS_QA_AUTOMATION/
├── Dynamic_Loading_Project/   # Módulo de pruebas con patrón POM
│   ├── locators.py            # Localizadores centralizados
│   └── test_main.py           # Script de prueba principal
├── reports/                   # Directorio raíz de evidencias y logs (Auto-generado)
│   └── RUN_YYYYMMDD_HHMMSS/   # Carpeta por sesión de ejecución
│       └── execution_summary.log
├── base_test.py               # Clase Maestra de Selenium (Lógica Core e Introspección)
├── config.py                  # Configuración global y variables de entorno
├── requirements.txt           # Dependencias de Python
└── run_tests.py               # Orquestador y ejecutor inteligente de la suite

Cómo Ejecutar las Pruebas
Clonar el repositorio:

Bash
git clone [https://github.com/tu-perfil/qa-automation-selenium-python.git](https://github.com/tu-perfil/qa-automation-selenium-python.git)
Instalar dependencias:

Bash
pip install -r requirements.txt
Configurar el Modo de Ejecución:

Abre config.py y define HEADLESS = True para ejecuciones rápidas en segundo plano, o False si deseas ver la interfaz gráfica del navegador.

Ejecutar la suite completa:

Bash
python run_tests.py
📊 Ejemplo de Reporte en Consola
Plaintext
============================================================
🚀 QA AUTOMATION FRAMEWORK - TEST SUITE RUNNER
Ejecución iniciada: 2026-10-12 16:48:57
ID de Sesión: RUN_20261012_164857
Archivos detectados: 2
============================================================

🚀 Iniciando ejecución (Modo Headless Activo)

✅ [FINALIZADO]: test_main.py (62.26s)
✅ [FINALIZADO]: manejo_spinner.py (60.23s)

============================================================
📊 RESUMEN DE EJECUCIÓN
============================================================
Total de Pruebas: 2
Pasadas:         2 ✅
Fallidas:        0 ❌
Tiempo Total:    122.74 segundos
📁 Reporte de Evidencias:
.../reports/evidencias/RUN_20261012_164857
============================================================

📩 Contacto
¡Hola! Soy Pedro Rafael, entusiasta del Software Testing y la Automatización.

🛠️ Especialidad: Pruebas manuales y automatización con Python/Selenium.

📍 Ubicación: Monterrey, Nuevo León, México