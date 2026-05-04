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
            # Auto-descubrimiento inteligente: busca archivos de prueba en todo el árbol del proyecto.
            # Usamos un set para evitar duplicados si un archivo cumple ambos patrones.
            patterns = ["test_*.py", "manejo_*.py"]
            self.test_files = list({f for p in patterns for f in BASE_DIR.rglob(p)})
            
        self.results: List[Dict[str, Any]] = []
        self.run_id = datetime.now().strftime("RUN_%Y%m%d_%H%M%S")
        self.start_time: Optional[float] = None

    def _print_banner(self):
        banner = f"""
        {'='*60}
        🚀 QA AUTOMATION FRAMEWORK - TEST SUITE RUNNER
        Ejecución iniciada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ID de Sesión: {self.run_id}
        {'='*60}
        """
        print(banner)

    def _execute_test(self, test_path: Path) -> Dict[str, Any]:
        """Ejecuta un proceso de prueba individual y captura métricas."""
        test_name = test_path.name
        print(f"🧪 [EJECUTANDO]: {test_name}...", end="\r")
        
        # Inyectamos el directorio base en el PYTHONPATH para que los scripts
        # hijos encuentren config.py y otros módulos sin necesidad de sys.path.append
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
                timeout=180,  # Límite de 3 minutos por prueba
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
                "error": "La prueba excedió el tiempo máximo de ejecución."
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
        self.start_time = time.time()
        
        # Determinamos el número de trabajadores (máximo 4 para no saturar el sistema con navegadores)
        max_workers = min(os.cpu_count() or 1, 4)
        print(f"🚀 Iniciando ejecución paralela ({max_workers} hilos de ejecución)\n")

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Mapeamos los tests a futuros
            futures = {executor.submit(self._execute_test, test): test for test in self.test_files if test.exists()}
            
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
        
        # Guardamos el reporte en un archivo físico dentro del RUN actual
        report_path = EVIDENCIA_DIR / self.run_id / "execution_summary.log"
        try:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(summary)
        except Exception as e:
            print(f"⚠️  No se pudo guardar el archivo de log: {e}")

if __name__ == "__main__":
    # Si se deja vacío, buscará automáticamente todos los tests del proyecto
    orchestrator = TestOrchestrator()
    
    try:
        orchestrator.run_all()
    except KeyboardInterrupt:
        print("\n\n🛑 Ejecución cancelada por el usuario.")
        sys.exit(1)