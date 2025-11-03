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
  - `modelos.py` (dataclasses `Sala` e `Evento` com validações básicas)
  - `regras.py` (funções puras de validação e detecção de conflitos de horários)
  - `repositórios.py` (interfaces abstratas para persistência de salas e eventos)
  - `serviços.py` (funções de caso de uso sem I/O, usando as interfaces e regras)
- Sem alterar o fluxo atual da `main.py` (monólito interativo); próxima etapa é conectar o menu às novas funções.
