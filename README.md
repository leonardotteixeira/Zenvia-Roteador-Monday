# zenvia-roteador

Serviço HTTP em Flask que roteia conversas de WhatsApp recebidas via Zenvia para o atendente correto, consultando um board do Monday.com pelo número do remetente.

## Problem

A Zenvia recebe as mensagens de WhatsApp num número único, mas cada conversa precisa cair com o atendente certo — e essa relação número → atendente vive no Monday.com, não na Zenvia.

## Solution

Um serviço HTTP simples que a Zenvia consulta a cada mensagem recebida: ele busca o número no board do Monday.com e devolve o e-mail do atendente responsável, que a Zenvia usa pra rotear a conversa.

## Architecture

```text
WhatsApp
   |
Zenvia (webhook)
   |
zenvia-roteador  --  Monday.com API (busca por telefone)
   |
e-mail do atendente (roteamento na Zenvia)
```

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

## Status

Ferramenta interna, construída para resolver uma necessidade pontual de roteamento de atendimento no trabalho — não é uma ferramenta genérica de integração Zenvia/Monday, é específica para esse fluxo. Mantida aqui como parte do meu portfólio.
