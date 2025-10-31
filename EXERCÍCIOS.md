# Exercícios – Gerenciador de Salas

Este conjunto de exercícios é dividido em duas trilhas:

- Parte 1: Melhorias simples no código atual (prática incremental).
- Parte 2: Mudanças que expõem as dificuldades do desenho monolítico (motivação para refatorar).

## Regras gerais

- Linguagem: Python >= 3.13.
- Não adicionar dependências externas.
- Manter dados em memória (listas/dicts) como no projeto.
- Mensagens e comentários em PT-BR. Funções em snake_case.
- Faça pequenos commits e descreva no HISTORY.md o que mudou.

Arquivo de referência: `main.py` (menu interativo, operações sobre salas e eventos).

## Parte 1 – Melhorias simples e didáticas

Objetivo: treinar validações, funções utilitárias, listagens e pequenas refatorações sem mudar a arquitetura geral.

1. Nome de sala único (case-insensitive)
2. Título do evento com tamanho válido (impor 3 ≤ len(título) ≤ 60).
3. Não agendar no passado
4. Duração máxima de evento (limitar a duração máxima de um evento)
5. Imprimir as datas no formato `YYYY-MM-DD HH:MM`
6. Listagem com ordenação e filtros
   - Objetivo: enriquecer `listar_salas()` sem efeitos colaterais.
   - Tarefas:
     - Permitir ordenar por `id|nome|capacidade` (asc/desc) e filtrar por `capacidade_min`.
   - Entrada pode ser interativa simples (perguntar critério) sem alterar o estado.
7. Bloquear remoção de sala com eventos
8. Buscar salas por nome (substring)

## Parte 2 – Por que o monólito dificulta a manutenção?

Objetivo: propor mudanças globais/frequentes que, feitas no desenho atual (input/print espalhados e lógica acoplada), se tornam difíceis.
A ideia é sentir a dor e depois apontar a refatoração como solução.

1. Troca de formato de data para `DD/MM/YYYY HH:MM`
   - Experiência: mude o formato em TODO o sistema.
   - Perguntas-guia: quantos pontos precisam ser alterados? O que acontece se esquecer um?
   - Critério: tudo continua funcionando e listagens/entradas usam o novo formato.
   - Insight: strings de formato estão duplicadas; centralizar em utilitários facilita.
2. Nova regra global: eventos só em dias úteis (seg-sex)
   - Experiência: aplicar a regra em criação e atualização.
   - Perguntas-guia: quantos lugares tratam data? Há risco de divergência?
   - Critério: recusas corretas com `[erro]` e mensagem clara.
   - Insight: mesma regra repetida em vários fluxos indica necessidade de função pura reutilizável.
3. Outro canal de entrada: script não interativo
   - Experiência: querer agendar/cancelar chamando funções sem `input/print` (por exemplo, de um teste ou script).
   - Tarefas:
     - Tentar usar as funções atuais diretamente em código (sem digitar no console) e observar a dificuldade.
     - Em seguida, criar funções puras: `cadastrar_sala_puro`, `agendar_evento_puro`, `cancelar_evento_puro` que recebem parâmetros e retornam valores, sem _prints_ e sem _inputs_.
   - Insight: separar I/O da regra de negócio melhora testabilidade e reuso.
4. Localização de mensagens (PT-BR e EN)
   - Experiência: permitir que o sistema troque entre PT-BR e EN para mensagens.
   - Perguntas-guia: quantos prints precisam ser tocados? Há concatenação de strings que dificulta?
   - Critério: trocar um "idioma atual" reflete em todas as mensagens.
   - Insight: camadas de apresentação e domínios misturadas geram retrabalho.
5. Relatório por sala (horas agendadas no mês)
   - Experiência: somar duração dos eventos por sala e imprimir relatório filtrável por mês.
   - Perguntas-guia: onde colocar essa lógica? Ela depende de I/O?
   - Critério: cálculo correto e separado de entrada/saída.
   - Insight: funções puras e módulos por domínio (salas/eventos/utils) deixam claro onde cada regra vive.
6. Feature toggle: permitir eventos "colados" (fim == início)
   - Experiência: adicionar uma flag global (ex.: `PERMITIR_ENCOSTADOS = True`) que altera a regra de conflito.
   - Perguntas-guia: quantos pontos de conflito existem? A mudança é atômica?
   - Critério: ao trocar a flag, o comportamento de conflito muda em todos os fluxos.
   - Insight: uma única função de conflito torna a mudança local.
7. Refatoração opcional como solução
   - Proposta: mover regras de negócio para funções puras e, se o arquivo crescer, separar em `salas.py`, `eventos.py` e `utils.py`. O `main.py` fica só com o menu e I/O.
   - Critério: manter a interface interativa intacta; cobrir os casos acima com menos pontos de mudança.

## Como Trabalhar

- Pequenos commits por exercício; descreva no `HISTORY.md`.
- Não adicionar bibliotecas externas.
- Se fizer refatorações maiores, atualize `README.md` com breve explicação de como executar.

Bom estudo! O foco é sentir os pontos de atrito do monólito e, aos poucos, evoluir para um desenho mais testável e modular, sem perder a simplicidade didática.
