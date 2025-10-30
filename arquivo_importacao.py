import os
import pandas as pd
from datetime import date
import numpy as np # Usado para a coluna de data vazia

def encontrar_pasta_downloads():
    """
    Encontra o caminho para a pasta "Downloads" do usuário atual.
    """
    home_dir = os.path.expanduser("~")
    caminho_downloads = os.path.join(home_dir, "Downloads")
    return caminho_downloads

def criar_relatorio_importacao():
    """
    Carrega o 'relatorio_consolidado.xlsx' e cria o novo
    arquivo 'CR_-_Importacao_AAAA-MM-DD.xlsx' com as
    transformações especificadas.
    """
    
    # --- 1. Definição de Nomes e Caminhos ---
    pasta_downloads = encontrar_pasta_downloads()
    
    arquivo_origem = "relatorio_consolidado.xlsx"
    caminho_origem = os.path.join(pasta_downloads, arquivo_origem)
    
    # Gera o nome do arquivo final com a data de hoje
    data_hoje = date.today().strftime('%Y-%m-%d')
    arquivo_final = f"CR_-_Importacao_{data_hoje}.xlsx"
    caminho_final = os.path.join(pasta_downloads, arquivo_final)
    
    # Colunas que OBRIGATORIAMENTE precisam existir no arquivo de origem
    colunas_necessarias = [
        'Data Emissão', 'Data Vencimento', 'Valor (R$)', 'Nº Doc', 
        'Nome', 'Identif', 'Nosso Nº', 'TXID'
    ]

    try:
        # --- 2. Carregar o Arquivo de Origem ---
        print(f"Carregando arquivo de origem: {caminho_origem}")
        df_origem = pd.read_excel(caminho_origem)

        # Verificação de segurança: checa se todas as colunas existem
        for col in colunas_necessarias:
            if col not in df_origem.columns:
                print(f"\nERRO: A coluna '{col}' não foi encontrada no arquivo '{arquivo_origem}'.")
                print(f"Colunas encontradas: {df_origem.columns.tolist()}")
                return

        print("Arquivo de origem carregado. Iniciando transformações...")

        # --- 3. Criar o Novo DataFrame em branco ---
        df_novo = pd.DataFrame()

        # --- 4. Aplicar as Transformações (Coluna por Coluna) ---

        # Renomeações diretas
        df_novo['Data de Competência'] = df_origem['Data Emissão']
        df_novo['Data de Vencimento'] = df_origem['Data Vencimento']
        df_novo['Valor'] = df_origem['Valor (R$)']
        df_novo['Cliente/Fornecedor'] = df_origem['Nome']
        df_novo['CNPJ/CPF Cliente/Fornecedor'] = df_origem['Identif']

        # Coluna de Data vazia (pd.NaT = Not a Time, o 'nulo' para datas)
        df_novo['Data de Pagamento'] = pd.NaT

        # Colunas com valores estáticos (iguais para todas as linhas)
        df_novo['Categoria'] = "Prestação de Serviços - Honorários Advocatícios"
        df_novo['Centro de Custo'] = "Previdenciário"

        # --- Transformação "Descrição" (f-string complexa) ---
        # Ex: "Parcela 01/24"
        # 1. Garante que 'Nº Doc' é numérico para podermos usar 'max'
        #    errors='coerce' transforma erros (ex: texto) em 'Nulo' (NaN)
        doc_num = pd.to_numeric(df_origem['Nº Doc'], errors='coerce').fillna(0).astype(int)
        
        # 2. Cria cada parcelamento levando em conta o cliente.
        #    .transform() devolve o valor máximo para todas as linhas daquele cliente
        doc_max_por_cliente = doc_num.groupby(df_origem['Nome']).transform("count")
      
        # 3. Formata as strings para ter 2 dígitos (ex: 1 -> "01", 24 -> "24")
        parcela_atual_str = doc_num.astype(str).str.zfill(2)
        parcela_max_str = doc_max_por_cliente.astype(str).str.zfill(2)
        
        # 4. Combina tudo na f-string (formato de string do pandas)
        df_novo['Descrição'] = 'Parcela ' + parcela_atual_str + '/' + parcela_max_str

        # --- Transformação "Observações" (f-string simples) ---
        # Ex: "Nosso Nº: 25/106647-4 - Chave PIX: f67c45e72e2448f1b91965a7b78a7132"
        # 1. Garante que ambas as colunas são strings antes de somar
        nosso_num_str = df_origem['Nosso Nº'].astype(str)
        txid_str = df_origem['TXID'].astype(str)
        
        # 2. Combina as strings
        df_novo['Observações'] = f'Nosso Nº: ' + nosso_num_str + ' - Chave PIX: ' + txid_str

        # --- 5. Salvar o Novo Arquivo ---
        print("\nTransformações concluídas. Salvando arquivo final...")
        
        # Garante que as colunas estejam na ordem exata que você pediu
        ordem_final_colunas = [
            'Data de Competência', 'Data de Vencimento', 'Data de Pagamento',
            'Valor', 'Categoria', 'Descrição', 'Cliente/Fornecedor',
            'CNPJ/CPF Cliente/Fornecedor', 'Centro de Custo', 'Observações'
        ]
        df_novo = df_novo[ordem_final_colunas]

        # Altera os tipos de dados das colunas de data para o formato DD/MM/AAAA
        df_novo['Data de Competência'] = pd.to_datetime(df_novo['Data de Competência'], errors='coerce').dt.strftime('%d/%m/%Y')
        df_novo['Data de Vencimento'] = pd.to_datetime(df_novo['Data de Vencimento'], errors='coerce').dt.strftime('%d/%m/%Y')

        #Alterar o tipo da coluna CNPJ/CPF Cliente/Fornecedor para string
        df_novo['CNPJ/CPF Cliente/Fornecedor'] = (
            df_novo['CNPJ/CPF Cliente/Fornecedor']
            .astype(str)
            .str.replace('\.0$', '', regex=True)
            .str.zfill(11)
        )

        # Salva o arquivo Excel sem a coluna de índice do pandas
        df_novo.to_excel(caminho_final, index=False)
        
        print("\n--- SUCESSO! ---")
        print(f"O novo arquivo foi criado em:")
        print(f"{caminho_final}")
        # print("\n--- 5 primeiras linhas do novo arquivo ---")
        # print(df_novo.head())

    except FileNotFoundError:
        print(f"\nERRO: O arquivo de origem '{arquivo_origem}' não foi encontrado na pasta Downloads.")
    except KeyError as e:
        print(f"\nERRO: Faltou uma coluna no arquivo original. Detalhe: {e}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

# --- Ponto de entrada do script ---
if __name__ == "__main__":
    criar_relatorio_importacao()