from base_test import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestLogin(BaseTest):
    def run(self):
        """Ejecuta el flujo de login."""
        try:
            print("Accediendo al portal de login...")
            self.driver.get("https://the-internet.herokuapp.com/login")

            # Uso de esperas centralizadas en self.wait
            campo_usuario = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            campo_pass = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
            boton_login = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius")))

            print("Ingresando credenciales...")
            campo_usuario.send_keys("tomsmith")
            campo_pass.send_keys("SuperSecretPassword!")
            boton_login.click()

            mensaje_exito = self.wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
            
            assert "You logged into a secure area!" in mensaje_exito
            self.tomar_captura("login_exitoso")
            print("✅ LOGIN EXITOSO: El sistema permitió el acceso.")

        except Exception as e:
            self.atrapar_bug("error_login")
            raise e
        finally:
            self.teardown()

if __name__ == "__main__":
    with TestLogin() as test:
        test.run()