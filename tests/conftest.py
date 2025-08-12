import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    # Setup Chrome options (optional)
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment for headless mode

    # Initialize WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver

    # Teardown WebDriver
    driver.quit()
