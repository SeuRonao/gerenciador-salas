# Exercícios – Gerenciador de Salas (versão com DDD leve)

Agora o projeto já está estruturado por camadas:

- Domínio (`src/domínio/`): modelos, regras e serviços (sem I/O)
- Infra (`src/infra/`): repositórios em memória
- Aplicação (`src/app/`): `container` (composição) e `fachada` (UI -> domínio)
- UI (`src/main.py`): prompts/prints, chama a fachada e mantém as mensagens esperadas nos testes

Os exercícios abaixo foram atualizados para explorar esse desenho. A ideia é praticar a evolução incremental de regras no domínio e refinamentos na fachada, mantendo o UI simples.

## Regras gerais

- Python >= 3.13, sem dependências externas
- Dados em memória (listas/entidades), mensagens PT-BR, snake_case
- Commits pequenos e anotações no `HISTORY.md`

## Trilha A — Incremental (refino de regras e APIs)

1. Nome de sala único (case-insensitive)

   - Onde: serviço `cadastrar_sala` (ou regra pura auxiliar em `regras.py`)
   - Critério de aceitação: ao tentar cadastrar nome repetido (ignorando maiúsculas/minúsculas), a fachada retorna erro e a UI mantém a mensagem de erro consistente

2. Título do evento com tamanho válido (3–60)

   - Onde: `regras.py` (função `titulo_valido`) + uso em `agendar_evento` e `atualizar_evento`
   - Aceite: títulos menores que 3 ou maiores que 60 são recusados com mensagem específica

3. Não agendar no passado

   - Onde: `regras.py` função pura (usa `datetime.now()`), aplicada em `agendar_evento` / `atualizar_evento`
   - Aceite: início anterior ao “agora” é recusado

4. Duração máxima de evento

   - Onde: `regras.py` (`duracao_valida(inicio, fim, max_horas=8)`) + serviços
   - Aceite: rejeitar eventos com duração acima do limite configurável

5. Datas formatadas uniformemente

   - Onde: fachada (helpers `_parse_dt` e `formatar_dt` com constante de formato)
   - Aceite: ajustes não quebram os testes atuais; se necessário, criar uma listagem “formatada” paralela

6. Listagem avançada de salas (ordenar/filtrar)

   - Onde: novo serviço puro `listar_salas_avançado(repo, ordenar_por, ordem, capacidade_min)` + `listar_salas_filtrado_ui` na fachada
   - Aceite: UI consegue solicitar ordenação por `id|nome|capacidade`, asc/desc, e filtrar por capacidade mínima

7. Bloquear remoção de sala com eventos

   - Onde: serviço `remover_sala` (ou variante) consultando `evento_repo`
   - Aceite: sala com eventos não é removida; mensagem clara via fachada/UI

8. Buscar salas por nome (substring)
   - Onde: serviço puro `buscar_salas_por_nome` + `*_ui` na fachada
   - Aceite: case-insensitive, retorna DTOs das salas encontradas

## Trilha B — Avançada (mudanças transversais)

1. Trocar formato de data para `DD/MM/YYYY HH:MM`

   - Onde: uma constante na fachada + helpers centralizados
   - Aceite: mudar a constante ajusta parsing/prints; UI permanece simples

2. Nova regra global: eventos só em dias úteis

   - Onde: `regras.py` função `é_dia_util(dt)`; usada nos serviços
   - Aceite: criação e atualização recusam eventos fora de seg–sex

3. Uso programático (sem I/O)

   - Onde: expor “API” simples (pode ser direto via `fachada`) no README
   - Aceite: exemplos de código funcionam chamando fachada/serviços sem input/print

4. Localização de mensagens (PT-BR/EN)

   - Onde: fachada passa a retornar códigos de erro; UI resolve código -> string via dicionário de mensagens
   - Aceite: troca de idioma afeta todas as mensagens sem tocar regras

5. Relatório por sala (horas no mês)

   - Onde: serviço puro que soma `fim - inicio` por sala
   - Aceite: retorna dados prontos para imprimir; fachada faz parsing de `ano/mes`

6. Feature toggle: permitir eventos colados (fim == início)

   - Onde: parâmetro/constante em `regras.py` afetando a regra de conflito
   - Aceite: alternar a flag muda o comportamento em criação/atualização

7. Refinos DDD opcionais
   - DTOs: substituir dicts soltos por TypedDict ou dataclasses na fachada
   - Remover imports de `domínio.*` do `main.py` (ficar 100% dependente da fachada)
   - “listar_eventos_formatado_ui”: UI imprime apenas strings formatadas vindas da aplicação

## Como trabalhar

- Priorize as regras como serviços/_"regras puras"_ no domínio
- Faça o parsing e mensagens na fachada; mantenha a UI apenas orquestrando prompts e prints
- Para cada exercício, crie testes unitários no nível de domínio/fachada e evite mexer nos E2E, a menos que o comportamento visível mude

Bom estudo! Agora a proposta é evoluir o domínio e a fachada, com uma UI estável e simples, reforçando os benefícios do DDD leve adotado no projeto.
