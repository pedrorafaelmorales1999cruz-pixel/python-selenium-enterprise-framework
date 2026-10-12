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
    """Clase base de nivel empresarial para centralizar la configuración del WebDriver, 
    gestión de contextos por introspección y captura automática de evidencias.
    """
    driver: WebDriver
    wait: WebDriverWait
    
    def __init__(self, timeout: Optional[int] = None):
        # Usar timeout global del config si no se especifica uno local
        actual_timeout = timeout if timeout is not None else getattr(config, 'EXPLICIT_WAIT', 15)
        
        self.driver = None  # type: ignore
        
        options = EdgeOptions()
        
        # Modo Headless (segundo plano) con argumentos de estabilidad y renderizado completo
        if getattr(config, 'HEADLESS', False):
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        
        # --- BLINDAJE DE PRIVACIDAD Y SILENCIO DE LOGS ---
        options.add_argument("--disable-features=msSmartScreen")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        
        # Inicialización del WebDriver
        driver_instance = webdriver.Edge(options=options)
        self.driver = driver_instance
        
        # Maximizar solo si no estamos en modo headless estricto
        if not getattr(config, 'HEADLESS', False):
            driver_instance.maximize_window()
            
        self.wait = WebDriverWait(driver_instance, actual_timeout)

        # --- LÓGICA DE DETECCIÓN DE CONTEXTO AUTOMÁTICA (Introspección) ---
        caller_file = Path(inspect.getfile(self.__class__))
        self.script_name = caller_file.stem
        self.project_name = caller_file.parent.name
        
        # Identificación del Run (orquestador o ejecución manual)
        self.run_id = os.environ.get("TEST_RUN_ID", datetime.datetime.now().strftime("MANUAL_%Y%m%d_%H%M"))
        
        # Definir rutas estructuradas para evidencias de esta prueba específica
        self.path_base = config.EVIDENCIA_DIR / self.run_id / self.project_name / self.script_name
        (self.path_base / "success").mkdir(parents=True, exist_ok=True)
        (self.path_base / "bugs").mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        """Soporte para el patrón Context Manager ('with')."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garantiza el cierre seguro del navegador al salir del bloque."""
        self.teardown()

    def teardown(self):
        """Cierra la sesión del navegador de forma segura."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass

    def _gestor_capturas(self, tipo: str, descripcion: str, prefijo: str = "") -> str:
        """Helper interno para gestionar y almacenar archivos de evidencia."""
        if not self.driver:
            return ""
            
        carpeta = self.path_base / tipo
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
        """Registra una evidencia visual de un paso exitoso."""
        nombre = self._gestor_capturas("success", descripcion)
        if nombre:
            print(f"📸 Paso guardado: {nombre}")

    def atrapar_bug(self, nombre_falla: str):
        """Registra captura de pantalla y código fuente HTML ante un fallo crítico."""
        nombre = self._gestor_capturas("bugs", nombre_falla, "BUG_")
        
        if self.driver:
            try:
                source_path = self.path_base / "bugs" / f"SOURCE_{nombre_falla}.html"
                with open(source_path, "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
            except Exception:
                pass
            
        if nombre:
            print(f"🚨 BUG REGISTRADO EN: {self.path_base / 'bugs'}")