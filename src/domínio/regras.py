from datetime import datetime
from typing import Iterable

from .modelos import Evento


def validar_intervalo(inicio: datetime, fim: datetime) -> bool:
    """Retorna True se o intervalo [inicio, fim) é válido (fim > inicio)."""
    return isinstance(inicio, datetime) and isinstance(fim, datetime) and fim > inicio


def intervalos_sobrepostos(
    a_inicio: datetime, a_fim: datetime, b_inicio: datetime, b_fim: datetime
) -> bool:
    """Checa sobreposição estrita de intervalos de tempo [a_inicio, a_fim) e [b_inicio, b_fim).

    Não há sobreposição quando a_fim <= b_inicio OU a_inicio >= b_fim.
    Portanto, há sobreposição quando NÃO (a_fim <= b_inicio ou a_inicio >= b_fim).
    """
    if not (validar_intervalo(a_inicio, a_fim) and validar_intervalo(b_inicio, b_fim)):
        return False
    return not (a_fim <= b_inicio or a_inicio >= b_fim)


# TODO será que precisa dessa regra mesmo?
def encontrar_conflito(
    eventos: Iterable[Evento],
    sala_id: int,
    inicio: datetime,
    fim: datetime,
    ignorar_evento_id: int | None = None,
) -> Evento | None:
    """Retorna um evento conflitante na mesma sala, se houver.

    Percorre os `eventos` e retorna o primeiro `Evento` que:
    - pertence à `sala_id` informada, e
    - possui sobreposição com o intervalo [inicio, fim)
    - e não é o próprio evento (quando `ignorar_evento_id` é fornecido)
    Caso não haja conflito, retorna None.
    """
    for e in eventos:
        if e.sala_id != sala_id:
            continue
        if ignorar_evento_id is not None and e.id == ignorar_evento_id:
            continue
        if intervalos_sobrepostos(inicio, fim, e.inicio, e.fim):
            return e
    return None
