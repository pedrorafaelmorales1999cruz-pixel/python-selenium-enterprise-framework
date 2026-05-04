import os
import inspect
from typing import Optional
from selenium import webdriver
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options as EdgeOptions
from pathlib import Path
import datetime
import config

class BaseTest:
    """Clase base para centralizar la configuración del WebDriver y utilidades."""
    driver: WebDriver
    wait: WebDriverWait
    
    def __init__(self, timeout=15):
        # Configuración para limpiar la consola de errores del navegador
        # Al definir los tipos arriba, la inteligencia de VS Code se propaga 
        # a todos los scripts hijos automáticamente por herencia.
        self.driver = None  # type: ignore
        
        options = EdgeOptions()
        
        # Modo Headless (segundo plano)
        if config.HEADLESS:
            options.add_argument("--headless=new")
        
        # --- BLINDAJE DE PRIVACIDAD Y SILENCIO ---
        options.add_argument("--disable-features=msSmartScreen") # Desactiva rastreo de SmartScreen
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_argument("--disable-features=msSmartScreen") # Evita errores de SmartScreen
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        
        driver_instance = webdriver.Edge(options=options)
        self.driver = driver_instance
        
        # Al usar la instancia local 'driver_instance', Pylance sabe que no es None
        driver_instance.maximize_window()
        self.wait = WebDriverWait(driver_instance, timeout)

        # --- LÓGICA DE DETECCIÓN DE CONTEXTO AUTOMÁTICA (Wow Factor) ---
        # Usamos introspección para identificar qué script está heredando de BaseTest.
        # inspect.getfile(self.__class__) obtiene la ruta absoluta del archivo hijo.
        caller_file = Path(inspect.getfile(self.__class__))
        
        # Extraemos el nombre del archivo (script) y su carpeta contenedora (proyecto)
        self.script_name = caller_file.stem
        self.project_name = caller_file.parent.name
        
        # Identificación del Run (del orquestador o manual)
        self.run_id = os.environ.get("TEST_RUN_ID", datetime.datetime.now().strftime("MANUAL_%Y%m%d_%H%M"))
        
        # Definir rutas base para esta prueba específica
        self.path_base = config.EVIDENCIA_DIR / self.run_id / self.project_name / self.script_name
        (self.path_base / "success").mkdir(parents=True, exist_ok=True)
        (self.path_base / "bugs").mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        """Soporte para el patrón 'with'."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garantiza el cierre al salir del bloque 'with'."""
        self.teardown()

    def teardown(self):
        """Cierra el navegador de forma segura."""
        if self.driver:
            self.driver.quit()

    def _gestor_capturas(self, tipo: str, descripcion: str, prefijo: str = "") -> str:
        """Helper interno para gestionar el guardado de archivos."""
        # Verificación de seguridad para el driver
        if not self.driver:
            return ""
            
        # tipo: "success" o "bugs"
        carpeta = self.path_base / tipo
        
        # Usamos milisegundos para permitir múltiples capturas seguidas en errores
        timestamp = datetime.datetime.now().strftime("%H%M%S_%f")[:10]
        nombre_limpio = descripcion.replace(" ", "_").lower()
        nombre_archivo = f"{prefijo}{timestamp}_{nombre_limpio}.png"
        
        ruta_final = carpeta / nombre_archivo

        try:
            self.driver.save_screenshot(str(ruta_final))
            return nombre_archivo
        except Exception as e:
            print(f"❌ Error al guardar captura: {e}")
            return ""

    def tomar_captura(self, descripcion: str):
        """Registra una evidencia de un paso exitoso."""
        nombre = self._gestor_capturas("success", descripcion)
        if nombre: print(f"📸 Paso guardado: {nombre}")

    def atrapar_bug(self, nombre_falla: str):
        """Registra una captura y el código fuente ante un error."""
        # 1. Tomar captura de pantalla
        nombre = self._gestor_capturas("bugs", nombre_falla, "BUG_")
        
        # 2. Guardar el código fuente de la página (Evidencia técnica extra)
        if self.driver:
            try:
                source_path = self.path_base / "bugs" / f"SOURCE_{nombre_falla}.html"
                with open(source_path, "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
            except:
                pass
            
        if nombre: print(f"🚨 BUG REGISTRADO EN: {self.path_base / 'bugs'}")