import os
import pandas as pd

def encontrar_pasta_downloads():
    """
    Encontra o caminho para a pasta "Downloads" do usuário atual.
    """
    home_dir = os.path.expanduser("~")
    caminho_downloads = os.path.join(home_dir, "Downloads")
    return caminho_downloads

def combinar_dois_arquivos(
    nome_arquivo1, 
    nome_arquivo2, 
    coluna_chave1,  # <<< MUDANÇA AQUI
    coluna_chave2,  # <<< MUDANÇA AQUI
    nome_arquivo_final,
    linha_cabecalho1=1,
    linha_cabecalho2=1
):
    """
    Carrega dois arquivos Excel, combina-os usando colunas-chave
    com nomes diferentes e salva o resultado.
    """
    
    pasta_downloads = encontrar_pasta_downloads()
    
    caminho1 = os.path.join(pasta_downloads, nome_arquivo1)
    caminho2 = os.path.join(pasta_downloads, nome_arquivo2)
    caminho_saida = os.path.join(pasta_downloads, nome_arquivo_final)
    
    indice_cabecalho1 = linha_cabecalho1 - 1
    indice_cabecalho2 = linha_cabecalho2 - 1
    
    try:
        # --- ETAPA 1: Carregar os dois arquivos ---
        print(f"Carregando Arquivo 1: {nome_arquivo1}")
        df1 = pd.read_csv(caminho1, header=indice_cabecalho1, sep=';', encoding='latin-1')
        
        print(f"Carregando Arquivo 2: {nome_arquivo2}")
        df2 = pd.read_excel(caminho2, header=indice_cabecalho2)
        
        # --- ETAPA 2: Verificar as colunas-chave ---
        if coluna_chave1 not in df1.columns:
            print(f"\nERRO: A coluna '{coluna_chave1}' não foi encontrada no Arquivo 1.")
            print(f"Colunas disponíveis: {df1.columns.tolist()}")
            return
            
        if coluna_chave2 not in df2.columns:
            print(f"\nERRO: A coluna '{coluna_chave2}' não foi encontrada no Arquivo 2.")
            print(f"Colunas disponíveis: {df2.columns.tolist()}")
            return

        # --- ETAPA 3: Combinar (Merge) os arquivos ---
        print(f"\nCombinando Arquivo 1 (chave: '{coluna_chave1}') com Arquivo 2 (chave: '{coluna_chave2}')...")
        
        df_combinado = pd.merge(
            df1, 
            df2, 
            left_on=coluna_chave1,  # <<< CHAVE DO ARQUIVO 1
            right_on=coluna_chave2, # <<< CHAVE DO ARQUIVO 2
            how='inner' # Mantenha 'inner' ou mude para 'outer' se precisar
        )
        
        if df_combinado.empty:
            print("AVISO: A combinação resultou em uma tabela vazia.")
            print("Verifique se os dados nas colunas-chave realmente correspondem.")
            return
            
        # --- ETAPA 4: Limpeza (Remover coluna-chave duplicada) ---
        # Opcional, mas recomendado.
        # Estamos removendo a coluna do Arquivo 2 e mantendo a do Arquivo 1.
        try:
            df_combinado = df_combinado.drop(columns=[coluna_chave2])
            print(f"Coluna duplicada '{coluna_chave2}' removida.")
        except KeyError:
            pass # Isso pode acontecer em cenários de merge complexos, mas é raro.

        # --- ETAPA 5: Salvar o novo arquivo ---
        df_combinado.to_excel(caminho_saida, index=False)
        
        print("\n--- SUCESSO! ---")
        print(f"O novo arquivo combinado foi salvo em:")
        print(f"{caminho_saida}")
        print(f"Total de {len(df_combinado)} linhas combinadas.")

    except FileNotFoundError as e:
        print(f"\nERRO: Arquivo não encontrado. {e.filename}")
    except Exception as e:
        print(f"\nERRO inesperado: {e}")

# --- Exemplo de uso ---
if __name__ == "__main__":
    
    # --- CONFIGURE AQUI ---

    # 1. Os nomes dos seus arquivos de origem
    ARQUIVO_1 = "fileExport.csv"
    ARQUIVO_2 = "relatorioTitulos.xls"
    
    # 2. A coluna que eles têm em comum (com NOMES DIFERENTES)
    COLUNA_CHAVE_ARQ_1 = "Nome"     # <- Nome no Arquivo 1
    COLUNA_CHAVE_ARQ_2 = "Pagador"  # <- Nome no Arquivo 2
    
    # 3. Onde os cabeçalhos estão em cada arquivo (Linha do Excel)
    LINHA_HEADER_1 = 1
    LINHA_HEADER_2 = 18
    
    # 4. O nome do novo arquivo que você quer criar
    ARQUIVO_FINAL = "relatorio_consolidado.xlsx"

    # --- FIM DA CONFIGURAÇÃO ---
    
    combinar_dois_arquivos(
        ARQUIVO_1, 
        ARQUIVO_2, 
        COLUNA_CHAVE_ARQ_1, 
        COLUNA_CHAVE_ARQ_2,
        ARQUIVO_FINAL,
        linha_cabecalho1=LINHA_HEADER_1,
        linha_cabecalho2=LINHA_HEADER_2
    )