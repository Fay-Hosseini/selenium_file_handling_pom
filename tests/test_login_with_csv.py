# tests/test_login_with_csv.py
import pytest
from pathlib import Path
from pages.login_page import LoginPage
from utils.file_utils import read_csv_for_parametrize

# Path to CSV file
DATA_DIR = Path(__file__).parent.parent / "data"
CREDENTIALS_CSV = DATA_DIR / "credentials.csv"

# Load test data once at import time
test_data = read_csv_for_parametrize(CREDENTIALS_CSV)

@pytest.mark.parametrize("username,password,expected_success", test_data)
def test_login(driver, username, password, expected_success):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(username, password)
    flash_message = login_page.get_flash_message()

    if expected_success:
        assert "You logged into a secure area!" in flash_message
    else:
        assert (
            "Your username is invalid!" in flash_message
            or "Your password is invalid!" in flash_message
        )
