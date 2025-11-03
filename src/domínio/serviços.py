from dataclasses import replace
from datetime import datetime

from .modelos import Sala, Evento
from .regras import validar_intervalo, encontrar_conflito
from .repositórios import SalaRepository, EventoRepository


# ----------------------------
# Serviços para Salas (sem I/O)
# ----------------------------


def cadastrar_sala(repo: SalaRepository, nome: str, capacidade: int) -> Sala | None:
    """Cadastra uma sala após validações simples.

    Retorna a Sala criada ou None em caso de validação inválida.
    """
    nome = (nome or "").strip()
    if not nome:
        return None
    if not isinstance(capacidade, int) or capacidade <= 0:
        return None

    nova = Sala(id=repo.proximo_id(), nome=nome, capacidade=capacidade)
    return repo.adicionar(nova)


def listar_salas(repo: SalaRepository) -> list[Sala]:
    """Retorna a lista de salas cadastradas (ordenada por id)."""
    return sorted(repo.listar(), key=lambda s: s.id)


def remover_sala(repo: SalaRepository, sala_id: int) -> bool:
    """Remove uma sala por id. Retorna True se removeu."""
    return repo.remover(sala_id)


# ------------------------------
# Serviços para Eventos (sem I/O)
# ------------------------------


def agendar_evento(
    eventos: EventoRepository,
    salas: SalaRepository,
    sala_id: int,
    titulo: str,
    inicio: datetime,
    fim: datetime,
) -> Evento | None:
    """Agenda um novo evento se as regras permitirem.

    Regras:
    - sala deve existir
    - título não vazio
    - fim > início
    - não pode haver conflito de horário na mesma sala
    """
    if salas.obter_por_id(sala_id) is None:
        return None
    titulo = (titulo or "").strip()
    if not titulo:
        return None
    if not validar_intervalo(inicio, fim):
        return None

    existentes = eventos.listar_por_sala(sala_id)
    if encontrar_conflito(existentes, sala_id, inicio, fim) is not None:
        return None

    novo = Evento(
        id=eventos.proximo_id(),
        sala_id=sala_id,
        titulo=titulo,
        inicio=inicio,
        fim=fim,
    )
    return eventos.adicionar(novo)


def cancelar_evento(eventos: EventoRepository, evento_id: int) -> bool:
    """Cancela (remove) um evento por id."""
    return eventos.remover(evento_id)


def atualizar_evento(
    eventos: EventoRepository,
    salas: SalaRepository,
    evento_id: int,
    *,
    titulo: str | None = None,
    sala_id: int | None = None,
    inicio: datetime | None = None,
    fim: datetime | None = None,
) -> Evento | None:
    """Atualiza campos de um evento existente.

    Campos não informados são mantidos. Retorna o evento atualizado ou None
    se o evento não existir ou se alguma regra for violada.
    """
    atual = eventos.obter_por_id(evento_id)
    if atual is None:
        return None

    novo_titulo = titulo if titulo is not None else atual.titulo
    novo_titulo = (novo_titulo or "").strip()
    if not novo_titulo:
        return None

    novo_sala_id = sala_id if sala_id is not None else atual.sala_id
    if salas.obter_por_id(novo_sala_id) is None:
        return None

    novo_inicio = inicio if inicio is not None else atual.inicio
    novo_fim = fim if fim is not None else atual.fim
    if not validar_intervalo(novo_inicio, novo_fim):
        return None

    existentes = eventos.listar_por_sala(novo_sala_id)
    if encontrar_conflito(
        existentes, novo_sala_id, novo_inicio, novo_fim, ignorar_evento_id=atual.id
    ):
        return None

    atualizado = replace(
        atual,
        titulo=novo_titulo,
        sala_id=novo_sala_id,
        inicio=novo_inicio,
        fim=novo_fim,
    )
    return eventos.atualizar(atualizado)


def listar_eventos(eventos: EventoRepository) -> list[Evento]:
    """Lista eventos ordenando por (inicio, sala_id, id)."""
    return sorted(eventos.listar(), key=lambda e: (e.inicio, e.sala_id, e.id))
