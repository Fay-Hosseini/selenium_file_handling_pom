from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self,driver,timeout: int=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Navigation ---
    def visit(self,url: str):
        self.driver.get(url)

    # --- Element finders ---
    def find(self, by: By,value: str):
        """Wait until element is present in DOM and return it."""
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_visible(self,by: By,value: str):
        """Wait until element is visible and return it."""
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    # --- Actions ---
    def click(self,by:By, value: str):
        element = self.find_visible(by, value)
        element.click()
        return element

    def type(self, by:By, value:str, text: str, clear_first = True):
        element = self.find_visible(by,value)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def get_text(self, by:By, value:str):
        element = self.find_visible(by,value)
        return element.text

    def is_element_visible(self, by:By, value:str):
        try:
            self.driver.find_element(by, value)
            return True
        except:
            return False