# Selenium (Python) Project — File Handling Practice with POM

A small, runnable Selenium + Pytest project demonstrating Page Object Model (POM) and file handling (reading/writing). Includes: project structure, code for page objects, utilities for reading/writing CSV/JSON/text, and a sample test that reads input data and writes an output report.

---

## Project structure

```
selenium_file_handling_pom/
├── README.md
├── requirements.txt
├── pytest.ini
├── conftest.py
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── secure_area_page.py
├── utils/
│   └── file_utils.py
├── tests/
│   └── test_file_handling.py
└── data/
    └── sample_input.csv
```

---

## Quick notes

* Uses `selenium` + `webdriver-manager` so you don't need to manually manage browser drivers.
* Uses `pytest` for tests and fixtures.
* File handling utilities support reading CSV, reading JSON, writing text/CSV/JSON reports.
* Example test visits the-internet login page (a stable test site), verifies login, and demonstrates reading usernames/passwords from `data/sample_input.csv` and writing results to `output_report.csv`.

---

## requirements.txt

```text
selenium>=4.10.0
webdriver-manager>=4.0.0
pytest>=7.0.0
pandas>=2.0.0
```

---

## pytest.ini

```ini
[pytest]
addopts = -q
testpaths = tests
```

---

## README.md

````markdown
# Selenium File Handling Practice (POM)

Run:

1. Create virtualenv and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
````

2. Run tests:

   ```bash
   pytest -q
   ```

Output:

* Tests will create `output_report.csv` in the project root with results.

````

---

## conftest.py

```python
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

@pytest.fixture(scope="session")
def chrome_options():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return opts

@pytest.fixture(scope="function")
def driver(chrome_options):
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture()
def data_dir(tmp_path_factory):
    # returns a Path object for storing temporary outputs in each test session
    root = PROJECT_ROOT.parent / "data"
    return root
````

---

## pages/base\_page.py

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def visit(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click(self, by, value):
        el = self.find(by, value)
        el.click()
        return el

    def type(self, by, value, text):
        el = self.find(by, value)
        el.clear()
        el.send_keys(text)
        return el

    def get_text(self, by, value):
        el = self.find(by, value)
        return el.text
```

---

## pages/login\_page.py

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://the-internet.herokuapp.com/login"
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button.radius")
    FLASH = (By.ID, "flash")

    def load(self):
        self.visit(self.URL)

    def login(self, username, password):
        self.type(*self.USERNAME, text=username)
        self.type(*self.PASSWORD, text=password)
        self.click(*self.LOGIN_BTN)

    def get_flash_message(self):
        return self.get_text(*self.FLASH)
```

---

## pages/secure\_area\_page.py

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class SecureAreaPage(BasePage):
    LOGOUT_BTN = (By.CSS_SELECTOR, "a.button")

    def is_logged_in(self):
        try:
            self.find(*self.LOGOUT_BTN)
            return True
        except Exception:
            return False
```

---

## utils/file\_utils.py

```python
import csv
import json
from pathlib import Path
from typing import List, Dict

# Read a CSV file and return list of dicts
def read_csv_to_dicts(path: Path) -> List[Dict[str, str]]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

# Write a list of dicts to CSV (overwrites)
def write_dicts_to_csv(path: Path, rows: List[Dict[str, str]]):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

# Read JSON
def read_json(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Write JSON
def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

# Append a text line
def append_text_line(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text + "\n")
```

---

## data/sample\_input.csv

```csv
username,password,label
invalid_user,invalid_pass,invalid
tomsmith,SuperSecretPassword!,valid
```

*(Note: the `tomsmith` credentials are the well-known test credentials for the-internet.herokuapp.com.)*

---

## tests/test\_file\_handling.py

```python
from pathlib import Path
from pages.login_page import LoginPage
from pages.secure_area_page import SecureAreaPage
from utils.file_utils import read_csv_to_dicts, write_dicts_to_csv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_REPORT = PROJECT_ROOT / "output_report.csv"
INPUT_CSV = PROJECT_ROOT / "data" / "sample_input.csv"


def test_login_and_file_handling(driver, data_dir, tmp_path):
    # read data
    rows = read_csv_to_dicts(INPUT_CSV)

    results = []
    login = LoginPage(driver)
    secure = SecureAreaPage(driver)

    for row in rows:
        username = row.get('username')
        password = row.get('password')
        label = row.get('label')

        login.load()
        login.login(username, password)

        success = secure.is_logged_in()
        flash = login.get_flash_message()

        results.append({
            'username': username,
            'password': password,
            'label': label,
            'success': str(success),
            'flash': flash.strip()
        })

        # if logged in, log out to reset state
        if success:
            # try clicking logout if present
            try:
                driver.find_element_by_css_selector('a.button').click()
            except Exception:
                pass

    # write report to tmp path (or root) to inspect after the test
    out_path = tmp_path / "output_report.csv"
    write_dicts_to_csv(out_path, results)

    # basic assertion: we expect at least one row processed
    assert len(results) == len(rows)
```

Notes:

* The test uses `tmp_path` so the output is kept in pytest's temporary dir (no repo pollution). Change `out_path` to `OUTPUT_REPORT` if you want the file in the repo root.
* The test demonstrates reading CSV (credentials), performing browser actions (login attempts), collecting results, and writing CSV report.

---

## Tips & exercises to extend this project

1. Add JSON input support and a test that reads JSON test cases.
2. Add a utility to write a human-friendly HTML report summarizing test results.
3. Add screenshots on failure (use `driver.save_screenshot(...)`).
4. Parameterize tests with `@pytest.mark.parametrize` using input data.
5. Add logging and more robust exception handling in page objects.

---

If you'd like, I can:

* provide the project as downloadable ZIP,
* generate the files in this chat as separate files,
* or convert the test to use a different demo site.

Tell me which next step you'd like.
