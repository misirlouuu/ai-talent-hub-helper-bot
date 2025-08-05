import time
import pathlib
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ссылки на программы
META_INFO = {
    "AI": "https://abit.itmo.ru/program/master/ai",
    "AI Product": "https://abit.itmo.ru/program/master/ai_product"
}

# Скачивание PDF-файла с кнопки "Учебный план"
def download_with_selenium_colab(url, download_path="/content/downloads", button_text="Учебный план"):
    pathlib.Path(download_path).mkdir(parents=True, exist_ok=True)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{button_text}')]"))
        )
        button.click()
        time.sleep(6)
        files = list(pathlib.Path(download_path).glob("*.pdf"))
        return str(files[0]) if files else None
    finally:
        driver.quit()

# Извлечение текста с сайта ИТМО
def extract_text_from_sites():
    all_content = []
    for name, url in META_INFO.items():
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for tag in soup(["script", "style", "meta"]): tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            all_content.append(f"{name}:\n{text}")
        except Exception as e:
            all_content.append(f"{name}: ошибка: {e}")
    return "\n\n".join(all_content)
