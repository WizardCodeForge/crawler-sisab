from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    # Configurar o ChromeDriver usando WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver
