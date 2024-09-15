from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Configurar o ChromeDriver usando WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Caminho onde o CSV será salvo
pasta_download = 'C:\\Users\\LKeuu\\OneDrive\\Documentos\\CSV'  # Usar scape com \\ para especificar caminho
os.makedirs(pasta_download, exist_ok=True)

try:
    # Abra o site
    driver.get('https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/indicadores/indicadorCadastro.xhtml')

    # Imprimir o HTML da página para depuração
    print(driver.page_source)

    # Aguarde e selecione a caixa "Nível de visualização"
    try:
        nivel_visualizacao = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#selectLinha'))
        )
        from selenium.webdriver.support.ui import Select
        select_nivel_visualizacao = Select(nivel_visualizacao)
        select_nivel_visualizacao.select_by_value('ibge')  # Seleciona a opção com o valor 'ibge'
    except Exception as e:
        print("Erro ao selecionar 'Nível de visualização':", e)

    # Aguarde e selecione a caixa "Condição das Equipes"
    try:
        condicao_equipes = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#opacao-capitacao'))
        )
        select_condicao_equipes = Select(condicao_equipes)
        select_condicao_equipes.select_by_value('|HM|')  # Seleciona a opção com o valor '|HM|'
    except Exception as e:
        print("Erro ao selecionar 'Condição das Equipes':", e)

    # Aguarde e selecione a caixa "Competência"
    try:
        # Abra o menu suspenso de competências
        driver.find_element(By.CSS_SELECTOR, '.multiselect.dropdown-toggle').click()

        # Obtenha todas as opções de checkbox
        options = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.multiselect-container .checkbox input[type="checkbox"]'))
        )

        if options:
            # Encontrar o checkbox com o maior valor
            max_value_checkbox = max(options, key=lambda opt: int(opt.get_attribute('value')) if opt.get_attribute('value').isdigit() else -1)
            valor_desejado = max_value_checkbox.get_attribute('value')

            # Selecionar o checkbox com o maior valor
            if not max_value_checkbox.is_selected():
                max_value_checkbox.click()

            print(f"Checkbox selecionado com valor: {valor_desejado}")

            # Fechar o menu (se necessário)
            driver.find_element(By.CSS_SELECTOR, '.multiselect.dropdown-toggle').click()
        else:
            print("Nenhuma checkbox encontrada no menu 'Competência'")
    except Exception as e:
        print("Erro ao selecionar 'Competência':", e)

    # Clique no botão de download e selecione CSV
    try:
        # Clique no botão de download
        download_button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-group .btn'))
        )
        download_button.click()

        # Simular a chamada JavaScript para o download CSV
        js_script = """
        function simulateCsvDownload() {
            var element = document.querySelector('a[onclick*="j_idt85"]');
            if (element) {
                element.click();
            } else {
                console.error("Elemento de download CSV não encontrado.");
            }
        }
        simulateCsvDownload();
        """
        driver.execute_script(js_script)
        print("Opção CSV selecionada com sucesso.")
    except Exception as e:
        print("Erro ao clicar no botão de download ou selecionar a opção CSV:", e)
        driver.save_screenshot("screenshot.png")  # Salve uma captura de tela para depuração

    # Aguarde o download do CSV 
    time.sleep(300)  # Ajustar o tempo conforme necessário

    # Nome do arquivo CSV (ajuste conforme necessário)
    nome_arquivo_csv = 'relatorio.csv'  # Atualize se necessário
    caminho_csv = os.path.join(pasta_download, nome_arquivo_csv)

    # Verifique se o arquivo foi baixado
    if os.path.exists(caminho_csv):
        print(f"Arquivo CSV baixado com sucesso: {caminho_csv}")
    else:
        raise FileNotFoundError(f"O arquivo CSV não foi encontrado em: {caminho_csv}")

finally:
    # Fechar o driver
    driver.quit()
