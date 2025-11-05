from datetime import datetime
from typing import cast

from domínio.modelos import Evento
from domínio.regras import validar_intervalo, intervalos_sobrepostos, encontrar_conflito


def dt(hm: str) -> datetime:
    # Ajuda a criar datetimes em 2025-01-01 a partir de "HH:MM"
    h, m = map(int, hm.split(":"))
    return datetime(2025, 1, 1, h, m)


def test_validar_intervalo():
    assert validar_intervalo(dt("09:00"), dt("10:00")) is True
    assert validar_intervalo(dt("10:00"), dt("10:00")) is False
    assert validar_intervalo(dt("10:00"), dt("09:00")) is False
    # tipos errados (forçando tipagem via cast para não quebrar o type checker)
    assert validar_intervalo(cast(datetime, "x"), cast(datetime, "y")) is False


def test_intervalos_sobrepostos():
    # [9,10) x [10,11) => não sobrepõe (borda)
    assert (
        intervalos_sobrepostos(dt("09:00"), dt("10:00"), dt("10:00"), dt("11:00"))
        is False
    )
    # [9,10) x [9:30,9:45) => sobrepõe
    assert (
        intervalos_sobrepostos(dt("09:00"), dt("10:00"), dt("09:30"), dt("09:45"))
        is True
    )
    # entradas inválidas => False
    assert (
        intervalos_sobrepostos(dt("10:00"), dt("09:00"), dt("09:30"), dt("09:45"))
        is False
    )


def test_encontrar_conflito():
    eventos = [
        Evento(id=1, sala_id=1, titulo="A", inicio=dt("09:00"), fim=dt("10:00")),
        Evento(id=2, sala_id=2, titulo="B", inicio=dt("09:30"), fim=dt("10:30")),
        Evento(id=3, sala_id=1, titulo="C", inicio=dt("11:00"), fim=dt("12:00")),
    ]

    # Conflito na mesma sala
    c = encontrar_conflito(eventos, sala_id=1, inicio=dt("09:30"), fim=dt("09:45"))
    assert c is not None and c.id == 1

    # Sem conflito em outra sala
    assert (
        encontrar_conflito(eventos, sala_id=2, inicio=dt("10:30"), fim=dt("11:00"))
        is None
    )

    # Sem conflito por borda
    assert (
        encontrar_conflito(eventos, sala_id=1, inicio=dt("10:00"), fim=dt("10:30"))
        is None
    )

    # Ignora o próprio evento
    assert (
        encontrar_conflito(
            eventos, sala_id=1, inicio=dt("09:30"), fim=dt("09:45"), ignorar_evento_id=1
        )
        is None
    )
