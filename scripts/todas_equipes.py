from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def executar_todas_equipes(driver, pasta_download):
    try:
        driver.get('https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/indicadores/indicadorCadastro.xhtml')
        print(driver.page_source)

        try:
            nivel_visualizacao = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#selectLinha'))
            )
            from selenium.webdriver.support.ui import Select
            select_nivel_visualizacao = Select(nivel_visualizacao)
            select_nivel_visualizacao.select_by_value('ibge')
        except Exception as e:
            print("Erro ao selecionar 'Nível de visualização':", e)

        try:
            condicao_equipes = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#opacao-capitacao'))
            )
            select_condicao_equipes = Select(condicao_equipes)
            select_condicao_equipes.select_by_value('')
        except Exception as e:
            print("Erro ao selecionar 'Condição das Equipes':", e)

        try:
            driver.find_element(By.CSS_SELECTOR, '.multiselect.dropdown-toggle').click()
            options = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.multiselect-container .checkbox input[type="checkbox"]'))
            )

            if options:
                max_value_checkbox = max(options, key=lambda opt: int(opt.get_attribute('value')) if opt.get_attribute('value').isdigit() else -1)
                valor_desejado = max_value_checkbox.get_attribute('value')

                if not max_value_checkbox.is_selected():
                    max_value_checkbox.click()

                print(f"Checkbox selecionado com valor: {valor_desejado}")
                driver.find_element(By.CSS_SELECTOR, '.multiselect.dropdown-toggle').click()
            else:
                print("Nenhuma checkbox encontrada no menu 'Competência'")
        except Exception as e:
            print("Erro ao selecionar 'Competência':", e)

        try:
            download_button = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-group .btn.btn-app'))
            )
            download_button.click()
            csv_option = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "//a[text()='Csv']"))
            )
            csv_option.click()
        except Exception as e:
            print("Erro ao clicar no botão de download ou selecionar a opção CSV:", e)

        time.sleep(100)
        
        # Nome do arquivo CSV com o valor da checkbox
        nome_arquivo_csv = f'sisab_todas_equipes_{valor_desejado}.csv'
        caminho_csv = os.path.join(pasta_download, nome_arquivo_csv)

        if os.path.exists(caminho_csv):
            print(f"Arquivo CSV baixado com sucesso: {caminho_csv}")
        else:
            raise FileNotFoundError(f"O arquivo CSV não foi encontrado em: {caminho_csv}")

    finally:
        driver.quit()
