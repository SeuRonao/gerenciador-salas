# Gerenciador de Salas

Esse é um projeto para ensinar de forma didática como criar um sistema simples de gerenciamento de salas e eventos utilizando Python.

## Funcionalidades

- Salas
  - Cadastrar (nome e capacidade)
  - Remover por id
  - Buscar por id
  - Listar todas
- Eventos
  - Agendar (com validação de conflito por sala)
  - Atualizar (título, sala, início e fim)
  - Cancelar por id
  - Listar todos (ordenados por início)

## Como executar

Pré-requisitos:

- Python 3.13 ou superior (ver `pyproject.toml`)
- uv instalado [uv](https://docs.astral.sh/uv/)

Comandos:

- Executar diretamente com Python (simples):

```bash
python -m src.main
```

- Executar isolado com uv (recomendado para manter o ambiente limpo):

```bash
uv run python -m src.main
```

Observações:

- Este projeto não possui dependências externas (`dependencies = []`), então o `uv run` apenas garante um ambiente controlado sem precisar criar/ativar venv manualmente.
- Se preferir um ambiente virtual dedicado, você pode usar:

```bash
uv venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -m src.main
```

## Observações

O objetivo é ser didático e simples, ideal para iniciantes em programação Python. O código é comentado para facilitar o entendimento.

O histórico de versões e explicação sobre o que estamos fazendo está disponível no arquivo `HISTORY.md`.

Inicialmente, o projeto não utiliza banco de dados, como também boas práticas de programação, para manter a simplicidade e o foco no aprendizado dos conceitos básicos.
Futuramente, podemos evoluir o projeto para incluir essas melhorias e principalmente, mostrar o motivo de ser importante manter o código limpo e organizado.

## Arquitetura atual

Para facilitar a evolução, o núcleo do problema (salas, eventos e alocação) está modelado em `src/domínio/` e já há implementações em memória e um container simples:

- `modelos.py`: dataclasses `Sala` e `Evento`
- `regras.py`: funções puras para validar intervalos e detectar conflitos
- `repositórios.py`: interfaces abstratas (ABCs) para persistência de salas e eventos
- `serviços.py`: funções de caso de uso (sem I/O) como `cadastrar_sala`, `agendar_evento`, etc.

Infraestrutura em memória (produção):

- `src/infra/repos_memória.py`: repositórios em memória
  - `MemSalaRepository`
  - `MemEventoRepository`

Composição (container):

- `src/app/container.py`:
  - `criar_container_memória()` cria um container com instâncias independentes dos repositórios em memória.

Essa camada não faz input/print, nem conhece a forma de persistência. O arquivo `src/main.py` continua como um monólito interativo para fins didáticos; em passos seguintes, o menu poderá ser conectado aos serviços do domínio.

Façade de aplicação (UI -> domínio, sem I/O):

- `src/app/fachada.py`:
  - `cadastrar_sala_ui`, `agendar_evento_ui`, `cancelar_evento_ui`, `atualizar_evento_ui`, `listar_salas_ui`, `listar_eventos_ui`
  - Converte entradas de UI (strings) para tipos do domínio e retorna estruturas simples (objetos do domínio ou dicts/booleans)

Main integrado ao domínio (migração incremental):

- `src/main.py` foi adaptado para usar os serviços do domínio por meio de adaptadores internos de repositório que escrevem
  nas listas globais `SALAS`/`EVENTOS` (compatível com os testes E2E atuais):
  - Salas: cadastrar, listar, remover, buscar por id
  - Eventos: agendar, cancelar, atualizar, listar

Exemplo rápido (programático com container + serviços):

```python
from app.container import criar_container_memória
from domínio.serviços import cadastrar_sala, agendar_evento, listar_eventos
from datetime import datetime

c = criar_container_memória()

s = cadastrar_sala(c.sala_repo, nome="Sala 1", capacidade=10)
e = agendar_evento(
    c.evento_repo,
    c.sala_repo,
    sala_id=s.id,
    titulo="Reunião",
    inicio=datetime(2025, 1, 1, 9, 0),
    fim=datetime(2025, 1, 1, 10, 0),
)
print(listar_eventos(c.evento_repo))
```

Exemplo rápido (programático com fachada):

```python
from app.container import criar_container_memória
from app import fachada

c = criar_container_memória()
ok, sala_ou_erro = fachada.cadastrar_sala_ui(c, "Sala 1", "10")
ok, evt_ou_erro = fachada.agendar_evento_ui(c, "1", "Daily", "2025-01-01 09:00", "2025-01-01 09:15")
salas = fachada.listar_salas_ui(c)
eventos = fachada.listar_eventos_ui(c)
```

## Como usar (exemplo rápido)

1. Rode o programa e utilize o menu interativo.
2. Cadastre ao menos uma sala.
3. Agende um evento escolhendo a opção "Agendar evento".
4. Para listar eventos, use a opção "Listar eventos".
5. Para atualizar um evento, use a opção "Atualizar evento"; deixe campos em branco para manter o valor atual.
6. Para remover um evento, use a opção "Cancelar evento" e informe o id do evento.

Formato de data/hora solicitado:

- `YYYY-MM-DD HH:MM` (ex.: `2025-10-31 14:30`)

Regras de agendamento:

- A sala deve existir.
- O título não pode ser vazio.
- O horário de fim deve ser maior que o de início.
- Não pode haver sobreposição de horários para a mesma sala.

## Testes

Estrutura:

- Unitários do domínio e infraestrutura: `test/unitário/`
- Fixture compartilhada: `test/unitário/conftest.py` fornece `container_memoria`
- Ponta a ponta do menu interativo: `test/ponta_a_ponta/`

Executar a suíte:

```bash
uv run pytest -q
```

Observação: o projeto usa layout `src/` (ver `pyproject.toml` com `pythonpath = "src"`).
