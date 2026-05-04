from selenium.webdriver.common.by import By

class DynamicLoadingLocators:
    START_BUTTON = (By.CSS_SELECTOR, "#start button")
    LOADING_SPINNER = (By.ID, "loading")
    FINISH_TEXT = (By.ID, "finish")