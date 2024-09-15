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
pasta_download = 'caminho/para/pasta/downloads'
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
        checkboxes = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.multiselect-container .checkbox input[type="checkbox"]'))
        )

        if checkboxes:
            # Defina o valor da competência desejada (ajuste conforme necessário)
            valor_desejado = '202407'

            # Encontrar o checkbox com o valor desejado
            for checkbox in checkboxes:
                if checkbox.get_attribute('value') == valor_desejado:
                    if not checkbox.is_selected():
                        checkbox.click()
                    break
            print(f"Checkbox selecionado com valor: {valor_desejado}")

            # Fechar o menu (se necessário)
            driver.find_element(By.CSS_SELECTOR, '.multiselect.dropdown-toggle').click()
        else:
            print("Nenhuma checkbox encontrada no menu 'Competência'")
    except Exception as e:
        print("Erro ao selecionar 'Competência':", e)

    # Clique no botão de download
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#componente-download'))
        ).click()
    except Exception as e:
        print("Erro ao clicar no botão de download:", e)

    # Selecione a opção CSV no menu suspenso
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="CSV"]'))  # Ajuste conforme necessário
        ).click()
    except Exception as e:
        print("Erro ao selecionar o formato CSV:", e)

    # Aguarde o download do CSV (ajuste o tempo de espera conforme necessário)
    time.sleep(300)  # Ajuste o tempo de espera conforme necessário

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
