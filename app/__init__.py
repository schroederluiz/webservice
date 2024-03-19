import pandas as pd
from flask import Flask, request, jsonify
import hmac
import json
import hashlib
from datetime import datetime

app = Flask(__name__)

@app.route('/consultar', methods=['POST'])
def consultar():
    # Receber o JSON enviado pela aplicação
    dados_recebidos = request.json

    df = pd.read_excel("C:\\Users\\luiz.pereira\\Downloads\\planilha.xlsx")
    cnpj = int(dados_recebidos['cnpj'])  
    data_hora_cliente = (dados_recebidos['dataHoraISO'])

    resultado = consulta_atividade(cnpj, df, data_hora_cliente)

    if resultado.get('ativo', 0) == 1:
        resultado = json.dumps(resultado)
        token = resultado.encode('utf-8')
        token = hmac.new(token, token, hashlib.sha256)
        token_client = token.hexdigest()
        df.loc[(df['cnpj'] == cnpj) & (df['flg_ativo'] == 1), 'token'] = token_client
        campo_excel = df.loc[df['cnpj'] == cnpj, 'token'].values[0]
        df.to_excel("C:\\Users\\luiz.pereira\\Downloads\\planilha.xlsx", index=False)
        print("Token inserido para CNPJ:", cnpj, "Token:", token_client, "token inserido: ", campo_excel)
        return jsonify(token_client)
    else:
        return jsonify({"status": "erro", "mensagem": "A empresa não está ativa"}), 404

def consulta_atividade(cnpj, df, data_hora_cliente):
    # Filtra as linhas com o CNPJ e o flg_ativo corretos
    empresa = df[(df['cnpj'] == cnpj) & (df['flg_ativo'] == 1)]
    
    if not empresa.empty:
        # Verifica se a coluna 'dt_validade_token' está presente no DataFrame
        if 'dt_validade_token' in empresa.columns:
            # Converte a dataHoraISO para um objeto datetime
            data_hora_cliente_dt = datetime.fromisoformat(data_hora_cliente)
            
            # Converte a coluna 'dt_validade_token' para objetos datetime, se não estiverem vazias
            empresa.loc[:, 'dt_validade_token'] = pd.to_datetime(empresa['dt_validade_token'], errors='coerce')
            
            # Filtra as linhas onde 'dt_validade_token' é maior que 'data_hora_cliente_dt'
            empresa = empresa[empresa['dt_validade_token'] > data_hora_cliente_dt]
        
        # Se ainda houver registros após a filtragem
        if not empresa.empty:
            flg_ativo = int(empresa['flg_ativo'].values[0] == 1)
            ativo = {
                'cnpj': cnpj,  
                'ativo':  flg_ativo, # Convertendo para inteiro
                'data':  data_hora_cliente_dt.strftime("%Y-%m-%d %H:%M:%S")
            }
            return ativo
        else:
            # Retorna uma resposta indicando que a empresa não está ativa
            return {"status": "erro", "mensagem": "Empresa não está ativa para a data especificada"}
    else:
        # Retorna uma resposta indicando que a empresa não foi encontrada ou não está ativa
        return {"status": "erro", "mensagem": "Empresa não encontrada ou não está ativa"}


if __name__ == '__main__':
    app.run(debug=True)
