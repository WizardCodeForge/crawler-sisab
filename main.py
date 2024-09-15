from utils.setup_driver import setup_driver
from scripts.equipes_homologadas import executar_equipes_homologadas
from scripts.todas_equipes import executar_todas_equipes
import os

def main():
    driver = setup_driver()

    # Caminho onde o CSV será salvo
    pasta_download = 'C:\\Users\\LKeuu\\OneDrive\\Documentos\\CSV\\'  # Usar scape com \\ para especificar caminho
    os.makedirs(pasta_download, exist_ok=True)

    # Executar o primeiro script
    print("Gerando Relatório de Cadastros Vinculados (SISAB EQUIPES HOMOLOGADAS)")
    executar_equipes_homologadas(driver, pasta_download)

    # Reconfigurar o driver para o segundo script
    driver = setup_driver()

    # Executar o segundo script
    print("Gerando Relatório de Cadastros Vinculados (SISAB TODAS EQUIPES)")
    executar_todas_equipes(driver, pasta_download)

if __name__ == "__main__":
    main()
