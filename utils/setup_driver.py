from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()

    # Configurar o diretório de download
    pasta_download = 'C:\\Users\\LKeuu\\OneDrive\\Documentos\\projetos\\Crawler-Sisab\\import_csv_test'
    prefs = {
        "download.default_directory": pasta_download,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Configurar o ChromeDriver usando WebDriver Manager com opções personalizadas
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver
