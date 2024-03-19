import pandas as pd
from datetime import datetime

def atualizar_data_hora(df):
    # Obtém o dia atual da máquina
    dia_atual = datetime.now().strftime("%Y-%m-%d")
    
    # Define a hora, minuto e segundo como 04:00:00
    hora_manha = "04:00:00"
    
    # Concatena o dia atual com a hora, minuto e segundo definidos
    data_hora_atual = f"{dia_atual} {hora_manha}"
    
    # Substitui a data e hora atual em todos os registros onde o campo ID está preenchido
    # e o campo flg_ativo é igual a 1
    filtro = (df['ID'].notnull()) & (df['flg_ativo'] == 1)
    df.loc[filtro, 'dt_validade_token'] = data_hora_atual

# Carrega o arquivo Excel
df = pd.read_excel("C:\\Users\\Admin\\Downloads\\planilha.xlsx")

# Certifique-se de que a coluna dt_validade_token seja inicializada com tipo de dado 'object'
if 'dt_validade_token' not in df.columns:
    df['dt_validade_token'] = None

# Chama a função para atualizar a data e hora
atualizar_data_hora(df)

# Salva o DataFrame de volta no arquivo Excel
df.to_excel("C:\\Users\\Admin\\Downloads\\planilha.xlsx", index=False)
