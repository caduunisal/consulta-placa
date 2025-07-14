# Projeto: Consulta de Placa de Veículo via API
# Stack: Flask (Python), integração com API externa

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configurações da API
API_URL = "https://api.consultarplaca.com.br/v2/consultarPlaca"
API_USER = "kadu.unisal1@gmail.com"
API_PASS = "timbiras64512#1977!"


@app.route("/consulta", methods=["GET"])
def consultar_placa():
    placa = request.args.get("placa")

    if not placa:
        return jsonify({"erro": "Parâmetro 'placa' é obrigatório."}), 400

    headers = {
        "Authorization": f"Bearer {API_PASS}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{API_URL}?placa={placa}", headers=headers)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "erro": f"Erro na consulta: {response.status_code}",
                "detalhes": response.text
            }), response.status_code
    except Exception as e:
        return jsonify({"erro": "Erro interno ao consultar placa", "detalhes": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
