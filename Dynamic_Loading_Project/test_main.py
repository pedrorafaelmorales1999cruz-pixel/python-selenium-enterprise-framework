from base_test import BaseTest
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import DynamicLoadingLocators
import time

class TestDynamicLoading(BaseTest):
    def run(self):
        try:
            print("\n--- INICIANDO AUTOMATIZACIÓN PROFESIONAL ---")
            self.driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
            
            print("[STEP 1]: Localizando botón de inicio...")
            btn = self.wait.until(EC.element_to_be_clickable(DynamicLoadingLocators.START_BUTTON))
            btn.click()

            print("[STEP 2]: Esperando que el Spinner desaparezca...")
            self.wait.until(EC.invisibility_of_element_located(DynamicLoadingLocators.LOADING_SPINNER))

            print("[STEP 3]: Validando mensaje final...")
            resultado = self.wait.until(EC.visibility_of_element_located(DynamicLoadingLocators.FINISH_TEXT))
            
            assert resultado.text == "Hello World!", f"ERROR: Se obtuvo '{resultado.text}'"
            
            self.tomar_captura("prueba_exitosa")
            print(f"✅ ÉXITO: Mensaje '{resultado.text}' validado.")

        except TimeoutException:
            print("\n❌ ERROR: Timeout en la página.")
            self.atrapar_bug("timeout_dinamico")
            raise
        except Exception as e:
            self.atrapar_bug("error_inesperado")
            print(f"\n❌ ERROR: {e}")
            raise
        finally:
            print("--- FINALIZANDO ---")
            self.teardown()

if __name__ == "__main__":
    with TestDynamicLoading() as test:
        test.run()