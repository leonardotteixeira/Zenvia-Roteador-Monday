from flask import Flask, request
import requests
import os

app = Flask(__name__)

MONDAY_TOKEN = os.environ.get("MONDAY_TOKEN")
BOARD_ID = 18403293983

def buscar_atendente(numero: str):
    numero = numero.replace("+", "").strip()
    
    query = """
    query {
        boards(ids: %d) {
            items_page(limit: 500) {
                items {
                    column_values {
                        column {
                            title
                        }
                        text
                    }
                }
            }
        }
    }
    """ % BOARD_ID

    headers = {
        "Authorization": MONDAY_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.monday.com/v2",
        json={"query": query},
        headers=headers
    )

    data = response.json()
    items = data["data"]["boards"][0]["items_page"]["items"]

    for item in items:
        telefone = ""
        email = ""
        for col in item["column_values"]:
            if col["column"]["title"].lower() == "telefone":
                telefone = col["text"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            if col["column"]["title"].lower() == "e-mail ai":
                email = col["text"]
        if telefone == numero or telefone == "55" + numero:
            print(f"Encontrado! Retornando: {email}")
            return email

    return None

@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.json
    print("Payload recebido:", data)
    try:
        numero = data.get("numero", "")
        email = buscar_atendente(numero)
        if email is None:
            print("Retornando: padrao")
            return "padrao", 200
        return email, 200
    except Exception as e:
        print(f"Erro: {e}")
        return "padrao", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)