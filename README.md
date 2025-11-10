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

Para facilitar a evolução, o núcleo do problema (salas, eventos e alocação) está modelado em `src/domínio/` e já há implementações em memória e um container simples. O fluxo completo hoje é:

UI (main.py) → Fachada (app/fachada.py) → Serviços de Domínio (domínio/serviços.py) → Repositórios (infra/repos_memória.py)

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

Essa camada (domínio) não faz input/print, nem conhece a forma de persistência.

Façade de aplicação (UI -> domínio, sem I/O):

- `src/app/fachada.py`:
  - `cadastrar_sala_ui`, `agendar_evento_ui`, `cancelar_evento_ui`, `atualizar_evento_ui`, `listar_salas_ui`, `listar_eventos_ui`
  - Converte entradas de UI (strings) para tipos do domínio e retorna estruturas simples (objetos do domínio ou dicts/booleans)

Main integrado ao domínio (sem globais):

- `src/main.py` usa diretamente o container de repositórios em memória (`criar_container_memória()`),
  sem variáveis globais de dados. Todos os fluxos interativos (input/print) foram preservados:
  - Salas: cadastrar, listar, remover, buscar por id
  - Eventos: agendar, cancelar, atualizar, listar

### Fluxo de dados (exemplo: agendar evento)

1. `main.criar_evento()` coleta entradas do usuário e delega para `fachada.agendar_evento_ui()`.
2. A fachada valida e converte strings (id, datas) e chama `serviços.agendar_evento(...)`.
3. O serviço consulta os repositórios do container (em memória), aplica regras (`regras.py`) e cria o evento.
4. O `main.py` imprime a resposta no formato didático (dict), preservando mensagens esperadas nos testes.

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

## Sugestões de melhoria (próximos passos leve-DDD)

1. Afinar fronteira UI ↔ aplicação

- Remover qualquer import de `domínio.*` em `main.py` (ficar só com `app.fachada` e `app.container`).
- Mover para a fachada o enriquecimento de listagem (ex.: `listar_eventos` já retornar linhas com nome da sala) para que o `main` apenas imprima.

2. Centralizar parsing na fachada

- Extrair helpers de parsing/validação (id, datetime) para a fachada e reaproveitar no `main` sem alterar ordem dos prompts/mensagens.

3. Tipos de retorno explícitos na aplicação

- Trocar dicts “soltos” por DTOs (TypedDict) na fachada: `SalaDTO`, `EventoDTO`. Mantém conteúdos iguais, facilita a leitura/IDE.

4. Testes unitários adicionais da fachada

- Cobrir cenários de `remover_sala_ui`, `buscar_sala_por_id_ui` e mais casos de `atualizar_evento_ui` (manter campos, conflito, intervalo inválido).

5. Documentação e CI

- README: incluir mini diagrama (como o fluxo acima) e tabelinha de mapeamento de mensagens (UI ↔ fachada).
- HISTORY: registrar as migrações para a fachada e retirada de globais.
- CI: workflow GitHub Actions com `pytest` e `ruff`.

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
