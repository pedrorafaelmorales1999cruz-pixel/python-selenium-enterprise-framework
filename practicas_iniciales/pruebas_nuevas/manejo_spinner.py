from base_test import BaseTest
from selenium.webdriver.support import expected_conditions as EC
from Dynamic_Loading_Project.locators import DynamicLoadingLocators

class TestSpinner(BaseTest):
    def run(self):
        try:
            self.driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
            
            boton_start = self.wait.until(EC.element_to_be_clickable(DynamicLoadingLocators.START_BUTTON))
            boton_start.click()
            
            self.wait.until(EC.invisibility_of_element_located(DynamicLoadingLocators.LOADING_SPINNER))
            
            texto_final = self.wait.until(EC.visibility_of_element_located(DynamicLoadingLocators.FINISH_TEXT)).text
            assert texto_final == "Hello World!", f"Error: {texto_final}"
            print("✅ PRUEBA EXITOSA.")
        except Exception as e:
            print(f"Fallo: {e}")
            raise
        finally:
            self.teardown()

if __name__ == "__main__":
    with TestSpinner() as test:
        test.run()