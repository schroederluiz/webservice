import pandas as pd
from flask import Flask, request, jsonify
import hmac
import json
import hashlib

app = Flask(__name__)

@app.route('/consultar', methods=['POST'])
def consultar():
    # Receber o JSON enviado pela aplicação
    dados_recebidos = request.json

    df = pd.read_excel("C:\\Users\\Admin\\Downloads\\planilha.xlsx")
    cnpj = int(dados_recebidos['cnpj'])  

    resultado = consulta_atividade(cnpj, df)

    if resultado.get('status') == "ok" and resultado.get('ativo', 0) == 1:
        resultado = json.dumps(resultado)
        token = resultado.encode('utf-8')
        token = hmac.new(token, token, hashlib.sha256)
        token_client = token.hexdigest()
        df.loc[(df['cnpj'] == cnpj) & (df['flg_ativo'] == 1), 'token'] = token_client
        campo_excel = df.loc[df['cnpj'] == cnpj, 'token'].values[0]
        df.to_excel("C:\\Users\\Admin\\Downloads\\planilha.xlsx", index=False)
        print("Token inserido para CNPJ:", cnpj, "Token:", token_client, "token inserido: ", campo_excel)
        return jsonify(token_client)
    else:
        return jsonify({"status": "erro", "mensagem": "A empresa não está ativa"}), 404

def consulta_atividade(cnpj, df):
    empresa = df[(df['cnpj'] == cnpj) & (df['flg_ativo'] == 1)]
    print(empresa)
    if not empresa.empty:
        flg_ativo = int(empresa['flg_ativo'].values[0] == 1)
        ativo = {
            'cnpj': cnpj,  
            'ativo':  flg_ativo # Convertendo para inteiro
        }
        return ativo
    else:
        # Retorna uma resposta indicando que a empresa não foi encontrada ou não está ativa
        return {"status": "erro", "mensagem": "Empresa não encontrada ou não está ativa"}

if __name__ == '__main__':
    app.run(debug=True)
