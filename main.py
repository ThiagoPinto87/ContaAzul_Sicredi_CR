import os
import combinar_arquivos
import arquivo_importacao

#---- 1º ETAPA ----
# Combinar arquivos
print("Iniciando a combinação de arquivos...")

def executar_combinar_arquivos():
    try:
        combinar_arquivos.combinar_dois_arquivos(
            nome_arquivo1="fileExport.csv",
            nome_arquivo2="relatorioTitulos.xls",
            coluna_chave1="Nome",
            coluna_chave2="Pagador",
            nome_arquivo_final="relatorio_consolidado.xlsx",
            linha_cabecalho1=1,
            linha_cabecalho2=18)
        print("Arquivo combinar_arquivos.py executado com sucesso.")
    except FileNotFoundError:
        print("Arquivo combinar_arquivos.py não encontrado.")


executar_combinar_arquivos()

#---- 2º ETAPA ----
# Criar o relatório de importação
print("\nIniciando a criação do relatório de importação...")
def executar_criar_relatorio_importacao():
    try:
        arquivo_importacao.criar_relatorio_importacao()
        print("Arquivo arquivo_importacao.py executado com sucesso.")
    except FileNotFoundError:
        print("Arquivo arquivo_importacao.py não encontrado.")


executar_criar_relatorio_importacao()


# ---- 3º ETAPA ----
# Deletar arquivo relatorio_consolidado.xlsx
def deletar_arquivo_relatorio_consolidado():

    caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    arquivo_relatorio = os.path.join(caminho_downloads, "relatorio_consolidado.xlsx")

    try:
        if os.path.exists(arquivo_relatorio):
            os.remove(arquivo_relatorio)
            print(f"Arquivo '{arquivo_relatorio}' deletado com sucesso.")
        else:
            print(f"Arquivo '{arquivo_relatorio}' não encontrado para deleção.")
    except Exception as e:
        print(f"Erro ao deletar o arquivo '{arquivo_relatorio}': {e}")

deletar_arquivo_relatorio_consolidado()

print()
print()
print("\nProcesso concluído com sucesso!")

#comando para criar o executável:
#pyinstaller --name="Vidotti_Ferreira_CR_CA_Importacao" --onefile --icon="ÍconeCaliber.ico" --hidden-import=pandas --hidden-import=openpyxl --hidden-import=numpy main.py