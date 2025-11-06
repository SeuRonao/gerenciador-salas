from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Any, Tuple

from domínio.serviços import (
    cadastrar_sala as _cadastrar_sala,
    listar_salas as _listar_salas,
    remover_sala as _remover_sala,
    agendar_evento as _agendar_evento,
    cancelar_evento as _cancelar_evento,
    atualizar_evento as _atualizar_evento,
    listar_eventos as _listar_eventos,
)
from domínio.regras import validar_intervalo, encontrar_conflito
from app.container import Container


FORMATO_DATETIME = "%Y-%m-%d %H:%M"


def _parse_int(texto: str) -> int | None:
    try:
        return int(texto)
    except (TypeError, ValueError):
        return None


def _parse_dt(texto: str) -> datetime | None:
    try:
        return datetime.strptime(texto, FORMATO_DATETIME)
    except (TypeError, ValueError):
        return None


# ----------------------------
# Operações de Sala (UI -> Domínio)
# ----------------------------


def cadastrar_sala_ui(
    container: Container, nome: str, capacidade_str: str
) -> Tuple[bool, Any]:
    cap = _parse_int(capacidade_str)
    if cap is None or cap <= 0:
        return False, "capacidade inválida"

    sala = _cadastrar_sala(container.sala_repo, nome, cap)
    if sala is None:
        return False, "dados inválidos para sala (nome/capacidade)"
    return True, sala


def listar_salas_ui(container: Container) -> list[dict]:
    salas = _listar_salas(container.sala_repo)
    # retorna estruturas simples (dict) para UI
    return [asdict(s) for s in salas]


def remover_sala_ui(container: Container, sala_id_str: str) -> tuple[bool, Any]:
    """Remove uma sala pelo id informado como string.

    Retorna (True, None) em caso de sucesso, ou (False, mensagem) em erro.
    """
    sala_id = _parse_int(sala_id_str)
    if sala_id is None or sala_id <= 0:
        return False, "id da sala inválido"

    ok = _remover_sala(container.sala_repo, sala_id)
    if ok:
        return True, None
    return False, "sala não encontrada"


# ------------------------------
# Operações de Evento (UI -> Domínio)
# ------------------------------


def agendar_evento_ui(
    container: Container,
    sala_id_str: str,
    titulo: str,
    inicio_str: str,
    fim_str: str,
) -> Tuple[bool, Any]:
    sala_id = _parse_int(sala_id_str)
    if sala_id is None or sala_id <= 0:
        return False, "id da sala inválido"

    inicio = _parse_dt(inicio_str)
    fim = _parse_dt(fim_str)
    if inicio is None or fim is None:
        return False, "formato de data inválido (YYYY-MM-DD HH:MM)"

    # Mensagens mais específicas quando possível
    if container.sala_repo.obter_por_id(sala_id) is None:
        return False, "sala não existe"
    if not (titulo or "").strip():
        return False, "título inválido"
    if not validar_intervalo(inicio, fim):
        return False, "intervalo de datas inválido"

    # Checa conflito antecipadamente para dar mensagem clara
    existentes = container.evento_repo.listar_por_sala(sala_id)
    if encontrar_conflito(existentes, sala_id, inicio, fim) is not None:
        return False, "conflito de horário"

    ev = _agendar_evento(
        container.evento_repo, container.sala_repo, sala_id, titulo, inicio, fim
    )
    if ev is None:
        # Fallback genérico (em cenários não diferenciáveis)
        return False, "não foi possível agendar o evento"
    return True, ev


def cancelar_evento_ui(container: Container, evento_id_str: str) -> Tuple[bool, Any]:
    evento_id = _parse_int(evento_id_str)
    if evento_id is None or evento_id <= 0:
        return False, "id do evento inválido"

    ok = _cancelar_evento(container.evento_repo, evento_id)
    if ok:
        return True, None
    return False, "evento não encontrado"


def atualizar_evento_ui(
    container: Container,
    evento_id_str: str,
    *,
    titulo: str | None = None,
    sala_id: str | None = None,
    inicio: str | None = None,
    fim: str | None = None,
) -> Tuple[bool, Any]:
    evento_id = _parse_int(evento_id_str)
    if evento_id is None or evento_id <= 0:
        return False, "id do evento inválido"

    sala_id_int: int | None
    if sala_id is None or sala_id == "":
        sala_id_int = None
    else:
        sala_id_int = _parse_int(sala_id)
        if sala_id_int is None or sala_id_int <= 0:
            return False, "id da sala inválido"

    inicio_dt: datetime | None
    if inicio is None or inicio == "":
        inicio_dt = None
    else:
        inicio_dt = _parse_dt(inicio)
        if inicio_dt is None:
            return False, "formato de data inválido (YYYY-MM-DD HH:MM)"

    fim_dt: datetime | None
    if fim is None or fim == "":
        fim_dt = None
    else:
        fim_dt = _parse_dt(fim)
        if fim_dt is None:
            return False, "formato de data inválido (YYYY-MM-DD HH:MM)"

    ev = _atualizar_evento(
        container.evento_repo,
        container.sala_repo,
        evento_id,
        titulo=titulo,
        sala_id=sala_id_int,
        inicio=inicio_dt,
        fim=fim_dt,
    )
    if ev is None:
        return False, "não foi possível atualizar o evento"
    return True, ev


def listar_eventos_ui(container: Container) -> list[dict]:
    eventos = _listar_eventos(container.evento_repo)
    return [
        {
            "id": e.id,
            "sala_id": e.sala_id,
            "titulo": e.titulo,
            "inicio": e.inicio,
            "fim": e.fim,
        }
        for e in eventos
    ]


def buscar_sala_por_id_ui(container: Container, sala_id_str: str) -> tuple[bool, Any]:
    """Obtém uma sala por id informado como string.

    Retorna (True, Sala) se encontrada, ou (False, mensagem) em caso de erro.
    """
    sala_id = _parse_int(sala_id_str)
    if sala_id is None or sala_id <= 0:
        return False, "id da sala inválido"
    s = container.sala_repo.obter_por_id(sala_id)
    if s is None:
        return False, "sala não encontrada"
    return True, s
