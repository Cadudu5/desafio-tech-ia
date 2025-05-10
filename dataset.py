import os
import pandas as pd

def unir_dataframes(diretorio, padrao_arquivo=None, ignorar_erros=True):
    """
    Une todos os DataFrames de arquivos em um diretório em um único DataFrame.
    
    Parâmetros:
    - diretorio: str, caminho do diretório contendo os arquivos
    - padrao_arquivo: str (opcional), padrão para filtrar arquivos (ex: '.csv')
    - ignorar_erros: bool, se True, ignora arquivos que não podem ser lidos
    
    Retorna:
    - DataFrame combinado ou None se nenhum arquivo válido for encontrado
    """
    # Lista para armazenar os DataFrames
    dataframes = []
    
    # Verifica se o diretório existe
    if not os.path.isdir(diretorio):
        raise ValueError(f"O diretório '{diretorio}' não existe.")
    
    # Percorre os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, arquivo)
        
        # Filtra por padrão de arquivo se especificado
        if padrao_arquivo and not arquivo.endswith(padrao_arquivo):
            continue
            
        # Tenta ler o arquivo como DataFrame
        try:
            # Detecta a extensão do arquivo para usar a função apropriada
            if arquivo.endswith('.csv'):
                df = pd.read_csv(caminho_completo)
            elif arquivo.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(caminho_completo)
            elif arquivo.endswith('.json'):
                df = pd.read_json(caminho_completo)
            elif arquivo.endswith('.parquet'):
                df = pd.read_parquet(caminho_completo)
            else:
                if not padrao_arquivo:  # Se não foi especificado um padrão, tenta ler como CSV
                    try:
                        df = pd.read_csv(caminho_completo)
                    except:
                        if not ignorar_erros:
                            raise
                        continue
                else:
                    continue
            
            # Adiciona uma coluna com o nome do arquivo de origem
            df['arquivo_origem'] = arquivo
            dataframes.append(df)
            
        except Exception as e:
            if not ignorar_erros:
                raise
            print(f"Erro ao ler o arquivo {arquivo}: {str(e)}")
            continue
    
    # Concatena todos os DataFrames se houver algum
    if dataframes:
        df_final = pd.concat(dataframes, ignore_index=True)
        print(f"União concluída. Total de linhas: {len(df_final)}")
        return df_final
    else:
        print("Nenhum arquivo válido encontrado no diretório.")
        return None

# Exemplo de uso:
if __name__ == "__main__":
    # Substitua pelo caminho do seu diretório
    diretorio = './data/raw/FOOD DATASET/'
    
    # Chama a função (opcional: especificar padrão de arquivo como '.csv')
    df_combinado = unir_dataframes(diretorio, padrao_arquivo='.csv')
    #dropando colunas desnecessárias
    df_combinado = df_combinado.drop(columns={"Unnamed: 0",
                                              "Unnamed: 0.1"})
    print(df_combinado.head())
    print(df_combinado.info())

    # Se quiser salvar o resultado em um novo arquivo
    if df_combinado is not None:
        df_combinado.to_csv('food_data_complete.csv', index=False)
        print("DataFrame combinado salvo como 'dados_combinados.csv'")