from utils.setup_driver import setup_driver
from scripts.equipes_homologadas import executar_equipes_homologadas
from scripts.todas_equipes import executar_todas_equipes
import os
import time

def main():
    # Caminho onde o CSV será salvo
    pasta_download = 'C:\\Users\\LKeuu\\OneDrive\\Documentos\\CSV\\'  # Usar scape com \\ para especificar caminho
    os.makedirs(pasta_download, exist_ok=True)

    # Inicializar o driver
    driver = setup_driver()

    try:
        # Executar o primeiro script
        print("Gerando Relatório de Cadastros Vinculados (SISAB EQUIPES HOMOLOGADAS)")
        executar_equipes_homologadas(driver, pasta_download)

    finally:
        # Fechar o driver após o primeiro script
        driver.quit()

    # Aguardar um pouco antes de reiniciar o driver
    time.sleep(10)

    # Inicializar o driver novamente
    driver = setup_driver()

    try:
        # Executar o segundo script
        print("Gerando Relatório de Cadastros Vinculados (SISAB TODAS EQUIPES)")
        executar_todas_equipes(driver, pasta_download)

    finally:
        # Fechar o driver após o segundo script
        driver.quit()

if __name__ == "__main__":
    main()
