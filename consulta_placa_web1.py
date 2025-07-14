# Projeto: Consulta de Placa de Veículo via API
# Stack: Flask (Python), integração com API externa + exibição simplificada

from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# Configurações da API
API_URL = "https://api.consultarplaca.com.br/v2/consultarPlaca"
API_USER = "kadu.unisal1@gmail.com"
API_PASS = "timbiras64512#1977!"

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
        <li><strong>Ano:</strong> {{ dados.get('ano') }}</li>
        <li><strong>Cor:</strong> {{ dados.get('cor') }}</li>
        <li><strong>Município:</strong> {{ dados.get('municipio') }}</li>
        <li><strong>Chassi:</strong> {{ dados.get('chassi') }}</li>
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
                    "marca": resp_json.get("marca", "N/A"),
                    "modelo": resp_json.get("modelo", "N/A"),
                    "ano": resp_json.get("ano", "N/A"),
                    "cor": resp_json.get("cor", "N/A"),
                    "municipio": resp_json.get("municipio", "N/A"),
                    "chassi": resp_json.get("chassi", "N/A")
                }
            else:
                erro = f"Erro na consulta: {response.status_code} - {response.text}"
        except Exception as e:
            erro = f"Erro interno: {str(e)}"

    return render_template_string(HTML_TEMPLATE, dados=dados, erro=erro)

if __name__ == "__main__":
    app.run(debug=True)
