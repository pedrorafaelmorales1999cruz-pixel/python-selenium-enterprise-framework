from base_test import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

class TestWikipedia(BaseTest):
    def run(self):
        try:
            # 1. Configuración (El driver ya está en self.driver gracias a BaseTest)
            self.driver.get("https://www.wikipedia.org")
            
            # 2. Localizar la barra de búsqueda e interactuar
            search_box = self.wait.until(EC.element_to_be_clickable((By.ID, "searchInput")))
            
            termino_busqueda = "Software Testing"
            print(f"Buscando: {termino_busqueda}...")
            
            search_box.send_keys(termino_busqueda)
            search_box.send_keys(Keys.RETURN)

            # 3. Esperar a que el título cargue
            self.wait.until(EC.title_contains("Software"))

            # 4. Validación profesional
            titulo_obtenido = self.driver.title.lower()
            print(f"Título validado: {titulo_obtenido}")

            assert "pruebas" in titulo_obtenido or "software" in titulo_obtenido, "El título no coincide"
            
            self.tomar_captura("wikipedia_exitosa")
            print("✅ PRUEBA WIKIPEDIA EXITOSA.")

        except Exception as e:
            self.atrapar_bug("error_wikipedia")
            raise e
        finally:
            self.teardown()

if __name__ == "__main__":
    with TestWikipedia() as test:
        test.run()