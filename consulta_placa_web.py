from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api.consultarplaca.com.br/v2/consultarPlaca"
API_USER = "kadu.unisal1@gmail.com"
API_PASS = "1ee5749a1b122bef69c0eaeee0d0dc2a"

@app.route("/consulta", methods=["GET"])
def consultar_placa():
    placa = request.args.get("placa")

    if not placa:
        return jsonify({"erro": "Parâmetro 'placa' é obrigatório."}), 400

    try:
        response = requests.get(
            API_URL,
            params={"placa": placa},
            auth=(API_USER, API_PASS)
        )

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
    app.run(debug=True, host="127.0.0.1", port=5050)
