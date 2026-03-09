from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

PLANILHA_PATH = "contatos.csv"

def carregar_planilha():
    df = pd.read_csv(PLANILHA_PATH, dtype=str)
    df["numero_whatsapp"] = df["numero_whatsapp"].str.replace(r"\D", "", regex=True)
    return df

def buscar_atendente(numero: str):
    df = carregar_planilha()
    numero = numero.replace("+", "").strip()
    resultado = df[df["numero_whatsapp"] == numero]
    if resultado.empty:
        return None
    return resultado.iloc[0].to_dict()

@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.json
    print("Payload recebido:", data)

    try:
        numero = data.get("numero", "")
        contato = buscar_atendente(numero)

        if contato is None:
            return "padrao", 200

        return contato["atendente_id"], 200

    except Exception as e:
        print(f"Erro: {e}")
        return "padrao", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)