# Gerenciador de Salas

Esse é um projeto para ensinar de forma didática como criar um sistema simples de gerenciamento de salas e eventos utilizando Python.

## Funcionalidades

- Cadastro de salas (criar, remover, buscar por id, listar)
- Agendamento de eventos (com validação de conflito por sala)
- Cancelamento de eventos

## Como executar

Pré-requisitos:

- Python 3.13 ou superior (ver `pyproject.toml`)
- uv instalado (https://docs.astral.sh/uv/)

Comandos:

- Executar diretamente com Python (simples):

```bash
python main.py
```

- Executar isolado com uv (recomendado para manter o ambiente limpo):

```bash
uv run python main.py
```

Observações:

- Este projeto não possui dependências externas (`dependencies = []`), então o `uv run` apenas garante um ambiente controlado sem precisar criar/ativar venv manualmente.
- Se preferir um ambiente virtual dedicado, você pode usar:

```bash
uv venv .venv
source .venv/bin/activate
python main.py
```

## Observações

O objetivo é ser didático e simples, ideal para iniciantes em programação Python. O código é comentado para facilitar o entendimento.

O histórico de versões e explicação sobre o que estamos fazendo está disponível no arquivo `HISTORY.md`.

Inicialmente, o projeto não utiliza banco de dados, como também boas práticas de programação, para manter a simplicidade e o foco no aprendizado dos conceitos básicos.
Futuramente, podemos evoluir o projeto para incluir essas melhorias e principalmente, mostrar o motivo de ser importante manter o código limpo e organizado.

## Como usar (exemplo rápido)

1. Rode o programa e utilize o menu interativo.
2. Cadastre ao menos uma sala.
3. Agende um evento escolhendo a opção "Agendar evento".
4. Para remover um evento, use a opção "Cancelar evento" e informe o id do evento listado.

Formato de data/hora solicitado:

- `YYYY-MM-DD HH:MM` (ex.: `2025-10-31 14:30`)

Regras de agendamento:

- A sala deve existir.
- O título não pode ser vazio.
- O horário de fim deve ser maior que o de início.
- Não pode haver sobreposição de horários para a mesma sala.
