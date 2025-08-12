from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://the-internet.herokuapp.com/login"

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")

    def load(self):
        self.visit(self.URL)

    def login(self, username: str, password: str):
        self.type(*self.USERNAME_INPUT, text = username)
        self.type(*self.PASSWORD_INPUT, text = password)
        self.click(*self.LOGIN_BUTTON)

    def get_flash_message(self) -> str:
        return self.get_text(*self.FLASH_MESSAGE)