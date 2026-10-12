import subprocess
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Optional, Any
from config import BASE_DIR, EVIDENCIA_DIR

class TestOrchestrator:
    """Orquestador de alto nivel para la ejecución y reporte de suites de automatización."""

    def __init__(self, test_files: Optional[List[str]] = None):
        if test_files:
            self.test_files = [BASE_DIR / f for f in test_files]
        else:
            # Auto-descubrimiento inteligente, quirúrgico y blindado:
            # Buscamos patrones específicos ignorando entornos virtuales, sistemas y carpetas externas.
            patterns = ["test_*.py", "manejo_*.py"]
            excluded_dirs = {
                ".venv", 
                "venv", 
                ".git", 
                "__pycache__", 
                "reports", 
                ".vs", 
                "qa-automation-selenium-python"
            }
            
            found_files = set()
            for pattern in patterns:
                for file_path in BASE_DIR.rglob(pattern):
                    # Validar que ninguna parte de la ruta contenga directorios excluidos
                    if any(excluded in file_path.parts for excluded in excluded_dirs):
                        continue
                    found_files.add(file_path)
            
            # Ordenamos alfabéticamente para mantener una ejecución estructurada
            self.test_files = sorted(list(found_files))
            
        self.results: List[Dict[str, Any]] = []
        self.run_id = datetime.now().strftime("RUN_%Y%m%d_%H%M%S")
        self.start_time: Optional[float] = None

    def _print_banner(self):
        banner = f"""
        {'='*60}
        🚀 QA AUTOMATION FRAMEWORK - TEST SUITE RUNNER
        Ejecución iniciada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ID de Sesión: {self.run_id}
        Archivos detectados: {len(self.test_files)}
        {'='*60}
        """
        print(banner)

    def _execute_test(self, test_path: Path) -> Dict[str, Any]:
        """Ejecuta un proceso de prueba individual de forma aislada y captura métricas."""
        test_name = test_path.name
        
        # Inyectamos el directorio base en el PYTHONPATH y pasamos el ID de sesión
        env = os.environ.copy()
        env["PYTHONPATH"] = str(BASE_DIR)
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["TEST_RUN_ID"] = self.run_id

        start = time.time()
        try:
            process = subprocess.run(
                [sys.executable, str(test_path.resolve())],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=180,  # Límite de seguridad de 3 minutos por script
                env=env
            )
            duration = time.time() - start
            return {
                "name": test_name,
                "status": "PASSED" if process.returncode == 0 else "FAILED",
                "duration": f"{duration:.2f}s",
                "error": process.stderr or process.stdout if process.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {
                "name": test_name,
                "status": "TIMEOUT",
                "duration": "180s",
                "error": "La prueba excedió el tiempo máximo de ejecución de 3 minutos."
            }
        except Exception as e:
            return {
                "name": test_name,
                "status": "CRASHED",
                "duration": "0s",
                "error": str(e)
            }

    def run_all(self):
        self._print_banner()
        
        if not self.test_files:
            print("⚠️ No se encontraron archivos de prueba válidos para ejecutar.")
            return

        self.start_time = time.time()
        
        # Limitamos a máximo 4 hilos para equilibrar rendimiento y recursos del navegador
        max_workers = 1  # Ejecución secuencial y estable para pruebas de navegador
        print(f"🚀 Iniciando ejecución paralela ({max_workers} hilos de ejecución)\n")

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._execute_test, test): test for test in self.test_files}
            
            for future in as_completed(futures):
                res = future.result()
                self.results.append(res)
                
                icon = "✅" if res["status"] == "PASSED" else "❌"
                print(f"{icon} [FINALIZADO]: {res['name']} ({res['duration']})")
                
                if res["status"] != "PASSED" and res["error"]:
                    error_lines = res["error"].strip().splitlines()
                    last_msg = error_lines[-1] if error_lines else "Error desconocido"
                    print(f"   ﹂ 🛑 Error: {last_msg}")

        self._print_summary()

    def _print_summary(self):
        total_duration = time.time() - (self.start_time or time.time())
        passed = sum(1 for r in self.results if r["status"] == "PASSED")
        failed = len(self.results) - passed

        summary = f"""
        {'='*60}
        📊 RESUMEN DE EJECUCIÓN
        {'='*60}
        Total de Pruebas: {len(self.results)}
        Pasadas:         {passed} ✅
        Fallidas:        {failed} ❌
        Tiempo Total:    {total_duration:.2f} segundos
        📁 Reporte de Evidencias:
        {EVIDENCIA_DIR.resolve() / self.run_id}
        {'='*60}
        """
        print(summary)
        
        # Persistencia del reporte consolidado en la carpeta de la sesión
        report_path = EVIDENCIA_DIR / self.run_id / "execution_summary.log"
        try:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(summary)
        except Exception as e:
            print(f"⚠️ No se pudo guardar el archivo de log: {e}")

if __name__ == "__main__":
    # Orquestador automático de la suite de QA
    orchestrator = TestOrchestrator()
    
    try:
        orchestrator.run_all()
    except KeyboardInterrupt:
        print("\n\n🛑 Ejecución cancelada por el usuario.")
        sys.exit(1)