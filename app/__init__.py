from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/consultar', methods=['POST'])
def consultar():
    # Receber o JSON enviado pela aplicação
    dados_recebidos = request.json

    df = pd.read_excel("C:\\Users\\luiz.pereira\\Downloads\\planilha.xlsx")
    cnpj = int(dados_recebidos['cnpj'])  

    resultado = consulta_atividade(cnpj, df)

    return jsonify(resultado)

    # Lógica para consultar o banco de dados e determinar se o cliente está ativo
    # Substitua esta lógica pela sua própria implementação

    # Exemplo de lógica simples que apenas verifica se o campo "ativo" está presente no JSON

def consulta_atividade(cnpj, df):
    empresa = df[df['cnpj'] == cnpj]
    flg_ativo = int(empresa['flg_ativo'].values[0] == 1)
    if not empresa.empty:
        ativo = {
            'cnpj': cnpj,  
            'ativo':  flg_ativo # Convertendo para inteiro
        }

        return ativo
    else:
        # Retorna uma resposta indicando que a empresa não foi encontrada
        return {"status": "erro", "mensagem": "Empresa não encontrada"}, 404

if __name__ == '__main__':
    app.run(debug=True)
