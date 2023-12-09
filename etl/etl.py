
import pandas as pd
import os 
import time


hr_inicio = time.time()

#diretorio
diretorio_data = r'c:\Users\frans\Documents\projetos\analise-scr-data\data'
diretorio_output = r'c:\Users\frans\Documents\projetos\analise-scr-data\output'

# Verifica se o diretório de saída existe, e se não, cria o diretório
if not os.path.exists(diretorio_output):
    os.makedirs(diretorio_output)

#lista vazia para armazenar os dataframes
lista_df = []

for planilha in os.listdir(diretorio_data):
    if planilha.endswith('.csv'):
        caminho_arquivo = os.path.join(diretorio_data,planilha)
        df = pd.read_csv(caminho_arquivo,delimiter = ";")
        df_credito = df[df['modalidade'] == 'PF - Cartão de crédito'].copy()
        colunas_numericas = ['a_vencer_ate_90_dias','a_vencer_de_91_ate_360_dias','a_vencer_de_361_ate_1080_dias',
        'a_vencer_de_1081_ate_1800_dias','a_vencer_de_1801_ate_5400_dias','a_vencer_acima_de_5400_dias',
        'vencido_acima_de_15_dias','carteira_ativa','carteira_inadimplida_arrastada','ativo_problematico']
        df_credito[colunas_numericas] = df_credito[colunas_numericas].apply(lambda x: x.str.replace(",", ".", regex=False).astype(float))
        #transformar o campo em formato de data
        df_credito['data_base'] = pd.to_datetime(df_credito['data_base'])
        #configurar o formato de float para duas casas decimais
        pd.set_option('display.float_format', lambda x: '%.2f' % x)        
        lista_df.append(df_credito)

df_final = pd.concat(lista_df,ignore_index= True)

# Caminho para o arquivo CSV de saída
caminho_output_csv = os.path.join(diretorio_output, 'planilhas_concatenadas.csv')

df_final.to_csv(caminho_output_csv)

#calcular o tempo final
hr_fim = time.time()
temp_process =  hr_fim - hr_inicio

print(f'Levou {temp_process} em segundos para processar os arquivos em csv')
