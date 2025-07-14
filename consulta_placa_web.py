# Projeto: Consulta de Placa de Veículo via API
# Stack: Flask (Python), integração com API externa

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Substitua pela URL real da API e sua chave (exemplo fictício abaixo)
API_URL = "https://api.consultarplaca.com.br/v1/veiculo"
API_KEY = "SUA_CHAVE_API_AQUI"

@app.route("/consulta", methods=["GET"])
def consultar_placa():
    placa = request.args.get("placa")

    if not placa:
        return jsonify({"erro": "Parâmetro 'placa' é obrigatório."}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
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
    app.run(debug=True)
