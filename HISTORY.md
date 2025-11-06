# Histórico de Commits

Todas as mudanças significativas neste projeto serão documentadas neste arquivo.

## v0.1.0

- Adicionado `.github/copilot-instructions.md` com orientações para agentes de IA trabalharem no projeto (escopo, padrões em memória e fluxo didático).
- Atualizado `README.md` com instruções de execução utilizando `uv` (opção recomendada para isolar o ambiente sem dependências externas).
- Criação/Leitura/Busca/Remoção/Listagem de salas implementado.

## v0.2.0

- Implementado agendamento de eventos em memória com validação de conflitos por sala.
- Adicionada função `criar_evento()` (fluxo interativo com input/print).
- Atualizado o menu com a opção "Agendar evento".
- Adicionada função `cancelar_evento()` para remover eventos por id.
- Atualizado o menu com a opção "Cancelar evento".
- Adicionada função `atualizar_evento()` para editar título, sala e horários com validações.
- Atualizado o menu com a opção "Atualizar evento".
- Adicionada função `listar_eventos()` para listar todos os eventos ordenados.
- Atualizado o menu com a opção "Listar eventos".

## v0.2.1

- Adicionado `EXERCÍCIOS.md` com duas trilhas de exercícios (melhorias simples e mudanças que evidenciam dificuldades do monólito).

## v0.2.2

- Adicionada suíte extensa de testes com `pytest` em `test/test_main.py` cobrindo:
- Cadastro, busca, listagem e remoção de salas
- Agendamento, cancelamento, atualização e listagem de eventos (inclui validações e conflitos)
- Saída imediata do menu
- Reset de estado global entre testes via fixture `autouse`

## v0.2.3

- Adotado layout `src/`: o arquivo `main.py` foi movido para `src/main.py`.
- Configuração do `pytest` define `pythonpath = "src"`, permitindo `import main` nos testes sem precisar `import src.main`.
- Ajustes de documentação: instruções de execução atualizadas para usar `python -m src.main` (ou via `uv`).

## v0.2.4

- Criada camada de domínio em `src/domínio` contendo:
  - `modelos.py` (_dataclasses_ `Sala` e `Evento` com validações básicas)
  - `regras.py` (funções puras de validação e detecção de conflitos de horários)
  - `repositórios.py` (interfaces abstratas para persistência de salas e eventos)
  - `serviços.py` (funções de caso de uso sem I/O, usando as interfaces e regras)
- Sem alterar o fluxo atual da `main.py` (monólito interativo); próxima etapa é conectar o menu às novas funções.

## v0.2.5

- Reorganização dos testes:
  - Testes de ponta a ponta do fluxo interativo movidos para `test/ponta_a_ponta/test_main.py`.
  - Nova suíte de testes unitários em `test/unitário/` cobrindo o domínio (`modelos.py`, `regras.py`, `repositórios.py`, `serviços.py`).
  - Ajustes menores para compatibilidade de tipagem nos testes (sem alterar código de produção).

## v0.2.6

- Adicionados repositórios em memória de produção em `src/infra/repos_memória.py`:
  - `MemSalaRepository` e `MemEventoRepository`, com operações básicas de CRUD, `proximo_id()` sequencial
    e retorno de cópias em `listar`/`listar_por_sala` para evitar mutação externa do estado interno.
- Adicionados testes unitários dedicados em `test/unitário/test_infra_repos_memória.py` cobrindo
  adicionar, listar, obter_por_id, atualizar, remover, `listar_por_sala` e comportamento de `proximo_id()`.
- Nenhuma alteração no `src/main.py`; este passo prepara o terreno para conectar o menu aos serviços do domínio
  via um container simples de composição em passos seguintes.

## v0.2.7

- Adicionado container de composição em `src/app/container.py` com a função `criar_container_memória()`.
- Adicionados testes do container em `test/unitário/test_container.py` garantindo tipos corretos, isolamento por instância
  e comportamento determinístico de `proximo_id()`.
- Adicionada fixture `container_memoria` em `test/unitário/conftest.py` para simplificar os testes.
- Adicionada façade de aplicação em `src/app/fachada.py` (sem I/O) com funções de alto nível para UI:
  `cadastrar_sala_ui`, `agendar_evento_ui`, `cancelar_evento_ui`, `atualizar_evento_ui`, `listar_salas_ui`, `listar_eventos_ui`.
- Adicionados testes da fachada em `test/unitário/test_fachada.py` cobrindo parsing, mensagens e integração com o domínio.
- Primeira migração incremental do `src/main.py` para usar o domínio (DDD) via adaptadores internos de repositório:
  - Salas: cadastrar, listar, remover, buscar por id
  - Eventos: agendar, cancelar, atualizar, listar
- Mantida compatibilidade com testes E2E e estado global (`SALAS`/`EVENTOS`), preparando terreno para futura remoção dos globais
  e uso direto do container.
