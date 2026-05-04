# 🚀 QA Automation Framework - Selenium & Python

![Python Version](https://img.shields.io/badge/python-3.14%2B-blue)
![Selenium](https://img.shields.io/badge/selenium-4.0%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

Este repositorio contiene un **Framework de Automatización de Pruebas E2E** profesional. Ha sido diseñado bajo principios de **Clean Code** y **Patrones de Diseño**, ofreciendo una solución escalable para la validación de aplicaciones web.

---

## 🛡️ Aviso de Seguridad y Privacidad
Este framework ha sido diseñado con un enfoque de **Privacidad Total** y **Seguridad del Entorno**:
*   **Ejecución 100% Local:** El código no realiza conexiones externas a servidores de terceros, no recolecta telemetría ni envía información de tu equipo a ninguna base de datos.
*   **Cero Rastreo de Rutas:** Se utiliza la librería `pathlib` para que todas las operaciones de archivos sean relativas al proyecto. No se filtran nombres de usuario de Windows ni rutas absolutas de tu disco duro en los logs.
*   **Aislamiento de Datos:** El archivo `.gitignore` bloquea la subida accidental de capturas de pantalla (evidencia) y archivos de configuración personal (`.env`), asegurando que tus datos sensibles nunca lleguen a repositorios públicos.
*   **Seguridad de Credenciales:** Nunca subas contraseñas reales al repositorio. Utiliza los ejemplos proporcionados con sitios de práctica seguros.
*   **Ejecución Aislada:** Se recomienda el uso de entornos virtuales (`venv`) para evitar conflictos con librerías del sistema.

---

## 🧠 Arquitectura: El "Wow Factor"
La pieza clave de este framework es su **Lógica de Introspección**. Mediante el uso de la librería `inspect`, la clase `BaseTest` identifica automáticamente qué script hijo la está invocando. Esto permite:
1.  Organizar evidencias automáticamente por Carpeta/Proyecto/Script sin configuración manual.
2.  Detectar el contexto de ejecución (Manual vs. Orquestado).
3.  Inyectar dependencias del WebDriver de forma transparente.

---

## 🌟 Características Principales
*   **Orquestador de Pruebas Centralizado:** Un motor inteligente (`run_tests.py`) que auto-descubre pruebas mediante patrones glob, gestiona la **ejecución paralela multinúcleo**, mide tiempos y genera reportes consolidados.
*   **Gestión Jerárquica de Evidencias:** Sistema automatizado que organiza capturas y código fuente HTML por `ID de Sesión / Proyecto / Script / {success o bugs}`.
*   **Modo Headless y Silencioso:** Configurable desde `config.py` para ejecuciones en segundo plano, ideal para servidores CI/CD.

## 🛠️ Tecnologías Utilizadas
*   **Lenguaje:** Python 3.10+
*   **Automatización:** Selenium WebDriver (Edge)
*   **Análisis Estático:** Pylance (Type Checking Mode: Basic/Strict)

## 📂 Estructura del Proyecto
```plaintext
PROYECTOS_QA_AUTOMATION/
├── Dynamic_Loading_Project/   # Proyecto con patrón POM
│   ├── locators.py            # Localizadores centralizados
│   └── test_main.py           # Script de prueba principal
├── reports/                   # Directorio raíz de evidencias (Auto-generado)
│   └── RUN_YYYYMMDD_HHMMSS/   # Carpeta por sesión de ejecución
├── base_test.py               # Clase Maestra de Selenium (Lógica Core)
├── config.py                  # Configuración global
├── requirements.txt           # Dependencias de Python
└── run_tests.py               # Orquestador y ejecutor de la suite
```

## ⚡ Cómo Ejecutar las Pruebas
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-perfil/qa-automation-selenium-python.git
   ```
2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
   > **Nota para mantenimiento:** Si instalas nuevas librerías, actualiza este archivo con:
   > ```bash
   > pip freeze > requirements.txt
   > ```

3. **Ejecutar la suite completa:**
   ```bash
   python run_tests.py
   ```

## 📊 Ejemplo de Reporte en Consola
```text
============================================================
🚀 QA AUTOMATION FRAMEWORK - TEST SUITE RUNNER
Ejecución iniciada: 2024-05-20 10:00:00
ID de Sesión: RUN_20240520_100000
============================================================

✅ [FINALIZADO]: test_main.py (14.25s)
✅ [FINALIZADO]: prueba_wikipedia.py (8.12s)
✅ [FINALIZADO]: prueba_login.py (7.34s)

============================================================
📊 RESUMEN DE EJECUCIÓN
============================================================
Total de Pruebas: 3
Pasadas:         3 ✅
Fallidas:        0 ❌
Tiempo Total:    29.71 segundos
📁 Reporte de Evidencias:
C:\Users\...\evidencia\RUN_20240520_100000
============================================================
```

---
### 💡 Tips para Reclutadores
> Este framework demuestra conocimientos en **Inyección de Dependencias**, **Variables de Entorno**, **Manejo de Procesos** y **Clean Code**. La separación de localizadores y la clase base facilitan la mantenibilidad a largo plazo.

---
## 📩 Contacto
¡Hola! Soy **Pedro Rafael**, entusiasta del Software Testing y la Automatización. 

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedrorafael-morales)

- 🛠️ Especialidad: Pruebas manuales y automatización con Python/Selenium.
- 📍 Ubicación: Monterrey, Nuevo León.