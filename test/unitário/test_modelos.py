import pytest
from datetime import datetime

from domínio.modelos import Sala, Evento


def test_sala_criação_ok():
    s = Sala(id=1, nome="Sala 1", capacidade=10)
    assert s.id == 1 and s.nome == "Sala 1" and s.capacidade == 10


@pytest.mark.parametrize(
    "kwargs,erro",
    [
        ({"id": 0, "nome": "A", "capacidade": 1}, "id da sala deve ser inteiro"),
        ({"id": 1, "nome": " ", "capacidade": 1}, "nome da sala não pode ser vazio"),
        ({"id": 1, "nome": "A", "capacidade": 0}, "capacidade deve ser inteiro"),
    ],
)
def test_sala_validações(kwargs, erro):
    with pytest.raises(ValueError) as exc:
        Sala(**kwargs)
    assert erro in str(exc.value)


def test_evento_criação_ok():
    ini = datetime(2025, 1, 1, 9, 0)
    fim = datetime(2025, 1, 1, 10, 0)
    e = Evento(id=1, sala_id=1, titulo="Reunião", inicio=ini, fim=fim)
    assert (
        e.id == 1
        and e.sala_id == 1
        and e.titulo == "Reunião"
        and e.inicio == ini
        and e.fim == fim
    )


@pytest.mark.parametrize(
    "kwargs,erro",
    [
        (
            dict(
                id=0,
                sala_id=1,
                titulo="A",
                inicio=datetime(2025, 1, 1, 9),
                fim=datetime(2025, 1, 1, 10),
            ),
            "id do evento deve ser inteiro",
        ),
        (
            dict(
                id=1,
                sala_id=0,
                titulo="A",
                inicio=datetime(2025, 1, 1, 9),
                fim=datetime(2025, 1, 1, 10),
            ),
            "sala_id deve ser inteiro",
        ),
        (
            dict(
                id=1,
                sala_id=1,
                titulo=" ",
                inicio=datetime(2025, 1, 1, 9),
                fim=datetime(2025, 1, 1, 10),
            ),
            "título do evento não pode ser vazio",
        ),
        (
            dict(id=1, sala_id=1, titulo="A", inicio="x", fim="y"),
            "inicio e fim devem ser datetime",
        ),
        (
            dict(
                id=1,
                sala_id=1,
                titulo="A",
                inicio=datetime(2025, 1, 1, 10),
                fim=datetime(2025, 1, 1, 9),
            ),
            "fim deve ser maior que início",
        ),
    ],
)
def test_evento_validações(kwargs, erro):
    with pytest.raises(ValueError) as exc:
        Evento(**kwargs)
    assert erro in str(exc.value)
