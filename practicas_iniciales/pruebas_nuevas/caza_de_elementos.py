from base_test import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestLocalizadores(BaseTest):
    def run(self):
        try:
            # 1. Ir a la página de Checkboxes
            self.driver.get("https://the-internet.herokuapp.com/checkboxes")
            print("Página de Checkboxes abierta.")

            check1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//form[@id='checkboxes']/input[1]")))
            
            if not check1.is_selected():
                print("Marcando el primer checkbox...")
                check1.click()

            # 2. Ir a la página de Inputs
            self.driver.get("https://the-internet.herokuapp.com/inputs")
            
            campo_numero = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
            valor_a_enviar = "12345"
            campo_numero.send_keys(valor_a_enviar)
            
            valor_final = campo_numero.get_attribute("value")
            assert valor_final == valor_a_enviar, f"Error: Se esperaba {valor_a_enviar} pero se obtuvo {valor_final}"
            print(f"✅ Número {valor_final} ingresado correctamente.")

            self.tomar_captura("practica_localizadores")

        except Exception as e:
            self.atrapar_bug("error_localizadores")
            raise e
        finally:
            self.teardown()

if __name__ == "__main__":
    with TestLocalizadores() as test:
        test.run()