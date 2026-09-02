# CLAUDE.md — guia para agentes de IA

Roteador de atendimento: recebe o número de quem escreveu no WhatsApp (via Zenvia) e devolve o e-mail do atendente responsável, consultando um board do Monday.com. O README descreve o fluxo completo — leia antes.

## Comandos

```bash
pip install -r requirements.txt
python app.py      # porta 8080, precisa de .env (copie de .env.example)
```

## Mapa do código

- `app.py` — único módulo: `buscar_atendente` consulta o board do Monday (GraphQL) e casa o número recebido com a coluna "Telefone"; a rota `POST /buscar` expõe isso para a Zenvia chamar.

## Regras que não podem quebrar

- Comparação de número tenta com e sem prefixo `55` (`buscar_atendente`) — números do Monday às vezes vêm sem o DDI.
- Em erro ou não-match, a rota sempre responde `"padrao"` (200 ou 500) em vez de propagar exceção — a Zenvia depende de sempre receber um destino válido.
- `MONDAY_TOKEN` só em variável de ambiente, nunca hardcoded.

## Convenções

- Projeto pequeno e de propósito único; não introduzir camadas (models, services) sem necessidade real.
