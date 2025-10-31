# Copilot instructions for gerenciador-salas

Purpose and scope

- Didactic Python project (PT-BR) to gerenciar salas e eventos.
- Current state: `main.py` apenas imprime uma saudação; funcionalidades previstas no `README.md` (cadastro/listagem de salas, agendamento/cancelamento de eventos).
- Sem banco de dados e sem dependências externas; use apenas estruturas em memória.

How to run and environment

- Requer Python >= 3.13 (ver `pyproject.toml`).
- Rodar localmente: `python main.py` na raiz do projeto.
- Dependências: `[]` por padrão; evite adicionar libs a menos que seja estritamente necessário para o objetivo didático.

Code organization (keep it simple)

- Mantenha o código claro, comentado e didático, com mensagens e comentários em PT-BR.
- Enquanto o projeto é pequeno, uma abordagem procedural com funções puras é preferida.
- Se o arquivo crescer, dividir por domínio é aceitável: ex.: `salas.py` (operações de salas) e `eventos.py` (agendamentos). Evite frameworks e ORMs.

Data and patterns (in-memory)

- Represente dados em estruturas simples (listas/dicts). Exemplos de formas úteis:
  - Sala: `{id, nome, capacidade}`
  - Evento: `{id, sala_id, titulo, inicio, fim}`
- Padrões comuns:
  - Cadastro: funções que recebem a coleção e os campos, validam e retornam o novo registro/ID.
  - Listagem: funções puras que filtram/ordenam sem efeitos colaterais.
  - Agendamento: valide conflito de horários por sala (intervalos sobrepostos de `inicio`/`fim`).
  - Cancelamento: remova por `id` com checagens simples.

Developer workflow

- Ao adicionar funcionalidades, atualize o `HISTORY.md` com um resumo curto das mudanças.
- Mantenha o `README.md` alinhado com as funcionalidades disponíveis (inclua exemplos de uso quando útil).
- Prefira nomes de funções em snake_case, parâmetros explícitos e retornos simples (bool/ID/dict).

Examples to follow

- Exemplos de funções sugeridas para manter consistência:
  - `def cadastrar_sala(salas, nome, capacidade) -> dict | None`
  - `def listar_salas(salas) -> list[dict]`
  - `def agendar_evento(eventos, salas, sala_id, titulo, inicio, fim) -> dict | None`
  - `def cancelar_evento(eventos, evento_id) -> bool`

Out of scope (for now)

- Não introduzir persistência, autenticação, CLI complexa, logs estruturados ou testes avançados sem necessidade didática clara.
