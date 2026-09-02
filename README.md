# zenvia-roteador

Serviço HTTP em Flask que roteia conversas de WhatsApp recebidas via Zenvia para o atendente correto, consultando um board do Monday.com pelo número do remetente.

## Como funciona

1. A Zenvia recebe uma mensagem de WhatsApp e chama `POST /buscar` com o número do remetente.
2. O serviço consulta a API GraphQL do Monday.com (`buscar_atendente`), varrendo os itens do board configurado e comparando a coluna "Telefone" com o número recebido (com e sem prefixo `55`).
3. Retorna o e-mail do atendente responsável (usado para rotear a conversa) ou `"padrao"` quando não há correspondência.

## Rodando localmente

```bash
pip install -r requirements.txt
cp .env.example .env   # preencher MONDAY_TOKEN
python app.py          # http://localhost:8080
```

## Endpoint

`POST /buscar`

```json
{ "numero": "19987485647" }
```

Resposta: e-mail do atendente (`text/plain`, 200) ou `"padrao"` (200 se não encontrado, 500 em erro).

## Deploy

Procfile pronto para Heroku (`gunicorn app:app`). Requer a variável de ambiente `MONDAY_TOKEN`.

## Stack

Python 3, Flask, Gunicorn, API do Monday.com (GraphQL).
