# SUGESTÕES DE TRABALHOS (DDD leve)

Este arquivo propõe temas de domínio semelhantes ao _"Gerenciador de Salas"_ para praticar com a mesma estrutura (domínio, infra, aplicação/fachada, UI).
Os escopos são didáticos, com foco em regras simples, validações e conflitos de agendamento/capacidade.

## Requisitos gerais (para qualquer trabalho)

- Linguagem e ambiente
  - Python >= 3.13 (ver padrões no `pyproject.toml`)
  - Sem dependências externas (mantemos o projeto didático e reprodutível)
  - Dados em memória (listas/entidades), sem persistência real (se quiser utilize um arquivo `.json` simples ou `sqlite` para praticar persistência)
- Camadas e separação de responsabilidades (DDD leve)
  - Domínio (`src/domínio/`): modelos, regras puras e serviços (sem I/O)
  - Infra (`src/infra/`): repositórios em memória (implementações de interfaces do domínio)
  - Aplicação (`src/app/`): `container` (composição) e `fachada` (UI -> domínio; parsing/validações; mapeia mensagens)
  - UI (`src/main.py`): apenas prompts/prints; delega para a fachada
- Testes obrigatórios
  - Unitários para domínio (regras e serviços)
  - Unitários para infraestrutura (repositórios em memória)
  - Unitários/integração para a fachada (parsing e mensagens)
  - Ponta a ponta (menu interativo) cobrindo os fluxos principais
- Estilo e mensagens
  - Funções em snake_case, mensagens em PT-BR, código comentado
  - Manter formato de data padrão `YYYY-MM-DD HH:MM` (ou centralizado em constante)
- Documentação e histórico
  - Atualizar `README.md` com como executar e arquitetura
  - Registrar marcos no `HISTORY.md` (curto e objetivo)

## Padrão de dados (sugestão)

- Entidades do domínio como dataclasses (`modelos.py`) e/ou dicts na camada de aplicação
- Repositórios com interfaces no domínio (ex.: `XRepository`) e implementações em memória na infra
- Fachada pode retornar `tuple[bool, payload]` ou DTOs (TypedDict/dataclasses) para a UI

---

## sugestões de trabalhos

Cada sugestão segue um formato: objetivo, entidades, casos de uso, regras, testes mínimos e extensões opcionais.

### Biblioteca: Livros e Empréstimos

- Objetivo: gerenciar empréstimos de livros para usuários
- Entidades
  - Livro `{id, titulo, autor, exemplares}`
  - Usuário `{id, nome}`
  - Empréstimo `{id, livro_id, usuário_id, inicio, fim}`
- Casos de uso
  - Cadastrar/listar/buscar/remover livro e usuário
  - Realizar empréstimo e devolução
  - Listar empréstimos
- Regras
  - Não emprestar se não há exemplares disponíveis
  - Datas válidas (fim > inicio), não permitir no passado
  - Opcional: limite de empréstimos por usuário
- Testes mínimos
  - Domínio: disponibilidade, datas, limite
  - Fachada: parsing e mensagens
  - E2E: empréstimo e devolução no menu
- Extensões opcionais
  - Multas por atraso (cálculo puro)
  - Relatório de livros mais emprestados

### Agenda Médica: Médicos, Pacientes e Consultas

- Objetivo: agendar consultas sem conflito por médico
- Entidades
  - Médico `{id, nome, especialidade}`
  - Paciente `{id, nome}`
  - Consulta `{id, medico_id, paciente_id, inicio, fim}`
- Casos de uso
  - Cadastrar/listar/buscar/remover médico e paciente
  - Agendar, remarcar e cancelar consulta
- Regras
  - Sem sobreposição de horários por médico
  - Consultas apenas em dias úteis e horário comercial (opcional)
- Testes mínimos: conflito por médico, dias úteis, parsing de datas
- Extensões: relatório de consultas por médico/mês

### Restaurante: Mesas e Reservas

- Objetivo: reservar mesas considerando capacidade e horários
- Entidades
  - Mesa `{id, lugares}`
  - Reserva `{id, mesa_id, cliente, inicio, fim}`
- Casos de uso: CRUD de mesas, reservar/cancelar, listar reservas
- Regras
  - Conflito por mesa
  - Capacidade mínima (lugares >= tamanho do grupo)
  - Turnos opcionais (almoço/jantar) e buffers de limpeza
- Testes: conflito, capacidade, turnos/buffer

### Cursos e Turmas: Matrículas

- Objetivo: matricular alunos em turmas, respeitando capacidade e horários
- Entidades
  - Curso `{id, nome}`
  - Turma `{id, curso_id, capacidade, inicio, fim}`
  - Aluno `{id, nome}`
  - Matricula `{id, turma_id, aluno_id}`
- Regras
  - Capacidade da turma
  - Conflito de horário entre turmas do mesmo aluno
- Extensões: lista de espera, relatório de ocupação

### Locadora de Veículos: Veículos e Locações

- Objetivo: locar veículos garantindo disponibilidade
- Entidades
  - Veículo `{id, placa, categoria}`
  - Locação `{id, veiculo_id, cliente, inicio, fim}`
- Regras
  - Conflito por veículo (sem locar o mesmo carro em períodos sobrepostos)
  - Duração mínima/máxima
- Extensões: categorias com regras específicas

### Cinema: Salas, Filmes e Sessões

- Objetivo: programar sessões por sala
- Entidades
  - SalaCinema `{id, nome, capacidade}`
  - Filme `{id, titulo, duracao_min}`
  - Sessão `{id, sala_id, filme_id, inicio, fim}`
- Regras
  - Sem sobreposição de sessões por sala
  - Classificação indicativa (opcional, checar idade do cliente)
- Extensões: intervalos obrigatórios entre sessões

### Manutenções: Técnicos e Ordens

- Objetivo: agendar manutenções para técnicos
- Entidades
  - Técnico `{id, nome}`
  - Ordem `{id, titulo, prioridade}`
  - Agendamento `{id, técnico_id, ordem_id, inicio, fim}`
- Regras
  - Sem sobreposição de horários por técnico
  - Prioridade pode influenciar a aceitação (opcional)
- Extensões: SLA por prioridade

### Quadras Esportivas: Reservas

- Objetivo: reservar quadras por modalidade
- Entidades
  - Quadra `{id, tipo, cobertura}`
  - Reserva `{id, quadra_id, cliente, inicio, fim}`
- Regras
  - Conflito por quadra
  - Buffers entre reservas; manutenção de quadra (janela bloqueada)
- Extensões: relatório por tipo de quadra/mês

### Projetos e Tarefas: Planejamento

- Objetivo: planejar tarefas sem sobrecarregar responsáveis
- Entidades
  - Projeto `{id, nome}`
  - Tarefa `{id, projeto_id, responsável, inicio, fim}`
- Regras
  - Sem sobreposição de tarefas por responsável
  - Dependências entre tarefas (opcional)
- Extensões: WIP limit por responsável

### Workshops e Inscrições

- Objetivo: organizar workshops com inscrições e lotação
- Entidades
  - Workshop `{id, titulo, capacidade, inicio, fim}`
  - Participante `{id, nome}`
  - Inscrição `{id, workshop_id, participante_id}`
- Regras
  - Capacidade do workshop
  - Agenda do participante (não sobrepor workshops)
- Extensões: lista de espera, confirmação por prioridade

---

## Dicas de implementação (DDD leve)

- Coloque validações de formato e parsing na fachada (ex.: `_parse_int`, `_parse_dt`)
- Centralize mensagens/códigos de erro na fachada; UI apenas imprime
- Coloque regras de negócio no domínio (`regras.py`) e use-as nos serviços (`serviços.py`)
- Repositórios em memória retornam cópias em listagens para evitar mutações externas
- Mantenha os testes de ponta a ponta sem acessar estado interno: use os fluxos interativos

## Testes sugeridos (mínimos)

- Domínio
  - Regras de conflito, intervalos, capacidade, limites
  - Serviços: happy path e 1–2 erros principais
- Infra
  - Repositórios: adicionar/atualizar/remover/listar/obter_por_id, `proximo_id`
- Fachada
  - Parsing e mensagens (id inválido, datas inválidas, existe/não existe)
- Ponta a ponta
  - 1 fluxo completo de criação + listagem
  - 1 fluxo de erro (conflito/validação) com mensagem esperada

## Entregáveis

- Código em camadas (domínio/infra/app/ui) conforme este repositório
- Testes unitários e E2E passando
- `README.md` explicando execução, arquitetura e exemplos de uso
- `HISTORY.md` com marcos curtos das mudanças
