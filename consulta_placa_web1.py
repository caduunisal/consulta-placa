# Projeto: Consulta de Placa de Veículo via API
# Stack: Flask (Python), integração com API externa + exibição simplificada

from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

# Configurações da API
API_URL = "https://api.consultarplaca.com.br/v2/consultarPlaca"
API_USER = "kadu.unisal1@gmail.com"
API_PASS = "1ee5749a1b122bef69c0eaeee0d0dc2a"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Consulta de Placa</title>
</head>
<body>
    <h1>Consulta de Placa</h1>
    <form method="get">
        <input name="placa" placeholder="Digite a placa" required>
        <button type="submit">Consultar</button>
    </form>

    {% if dados %}
    <h2>Resultado:</h2>
    <ul>
        <li><strong>Placa:</strong> {{ dados.get('placa') }}</li>
        <li><strong>Marca:</strong> {{ dados.get('marca') }}</li>
        <li><strong>Modelo:</strong> {{ dados.get('modelo') }}</li>
        <li><strong>Ano Fabricacao:</strong> {{ dados.get('ano_fabricacao') }}</li>
        <li><strong>Ano Modelo:</strong> {{ dados.get('ano_modelo') }}</li>
        <li><strong>Cor:</strong> {{ dados.get('cor') }}</li>
        <li><strong>Município:</strong> {{ dados.get('municipio') }}</li>
        <li><strong>Chassi:</strong> {{ dados.get('chassi') }}</li>
        <li><strong>Sub Segmento:</strong> {{ dados.get('sub_seg') }}</li>
    </ul>
    {% endif %}

    {% if erro %}
    <p style="color:red;">Erro: {{ erro }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/consulta", methods=["GET"])
def consultar_placa():
    placa = request.args.get("placa")
    dados = {}
    erro = None

    if placa:
        try:
            response = requests.get(
                API_URL,
                params={"placa": placa},
                auth=(API_USER, API_PASS)
            )
            if response.status_code == 200:
                
                resp_json = response.json()
                dados = {
                    "placa": placa,
                    "marca": resp_json.get("dados", {}).get("informacoes_veiculo", {}).get("dados_veiculo").get("marca", "N/A"),
                    "modelo": resp_json.get("dados", {}).get("informacoes_veiculo", {}).get("dados_veiculo").get("modelo", "N/A"),
                    "ano_fabricacao": resp_json.get("dados", {}).get("informacoes_veiculo", {}).get("dados_veiculo").get("ano_fabricacao", "N/A"),
                    "ano_modelo": resp_json.get("dados", {}).get("informacoes_veiculo", {}).get("dados_veiculo").get("ano_modelo", "N/A"),
                    "cor": resp_json.get("dados", {}).get("informacoes_veiculo", {}).get("dados_veiculo").get("cor", "N/A"),
                    "municipio": resp_json.get("dados", {}).get("informacoes_veiculo", {}).get("dados_veiculo").get("municipio", "N/A"),
                    "chassi": resp_json.get("dados", {}).get("informacoes_veiculo", {}).get("dados_veiculo").get("chassi", "N/A"),
                    "sub_seg": resp_json.get("dados", {}).get("informacoes_veiculo", {}).get("dados_tecnicos").get("sub_segmento", "N/A")
                }
                print(json.dumps(resp_json, indent=2))
            else:
                erro = f"Erro na consulta: {response.status_code} - {response.text}"
        except Exception as e:
            erro = f"Erro interno: {str(e)}"

    return render_template_string(HTML_TEMPLATE, dados=dados, erro=erro)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5050)
