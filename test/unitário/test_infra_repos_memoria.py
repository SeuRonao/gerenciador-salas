from datetime import datetime


from domínio.modelos import Sala, Evento

from infra.repos_memoria import MemSalaRepository, MemEventoRepository  # type: ignore


def dt(hm: str) -> datetime:
    h, m = map(int, hm.split(":"))
    return datetime(2025, 1, 1, h, m)


def test_mem_sala_repo_básico():
    rs = MemSalaRepository()

    # estado inicial
    assert rs.listar() == []
    assert rs.obter_por_id(1) is None
    assert rs.proximo_id() == 1

    # adicionar
    s1 = Sala(id=rs.proximo_id(), nome="Sala 1", capacidade=10)
    rs.adicionar(s1)
    assert rs.obter_por_id(1) == s1
    assert [s.id for s in rs.listar()] == [1]
    assert rs.proximo_id() == 2

    # atualizar
    s1x = Sala(id=1, nome="Sala 1X", capacidade=20)
    r = rs.atualizar(s1x)
    assert r is s1x
    assert rs.obter_por_id(1) == s1x

    # remover
    assert rs.remover(999) is False
    assert rs.remover(1) is True
    assert rs.listar() == []


def test_mem_evento_repo_básico():
    re = MemEventoRepository()

    # estado inicial
    assert re.listar() == []
    assert re.obter_por_id(1) is None
    assert re.proximo_id() == 1

    # adicionar
    e1 = Evento(
        id=re.proximo_id(), sala_id=1, titulo="A", inicio=dt("09:00"), fim=dt("10:00")
    )
    re.adicionar(e1)
    assert re.obter_por_id(1) == e1
    assert [e.id for e in re.listar()] == [1]
    assert [e.id for e in re.listar_por_sala(1)] == [1]
    assert re.listar_por_sala(2) == []
    assert re.proximo_id() == 2

    # atualizar
    e1x = Evento(id=1, sala_id=1, titulo="AX", inicio=dt("09:30"), fim=dt("10:30"))
    r = re.atualizar(e1x)
    assert r is e1x
    got = re.obter_por_id(1)
    assert got is not None and got.titulo == "AX" and got.inicio == dt("09:30")

    # remover
    assert re.remover(999) is False
    assert re.remover(1) is True
    assert re.listar() == []


def test_mem_evento_repo_listar_por_sala_nao_muda_estado():
    re = MemEventoRepository()

    e1 = Evento(
        id=re.proximo_id(), sala_id=1, titulo="A", inicio=dt("07:00"), fim=dt("08:00")
    )
    re.adicionar(e1)
    e2 = Evento(
        id=re.proximo_id(), sala_id=2, titulo="B", inicio=dt("07:00"), fim=dt("08:00")
    )
    re.adicionar(e2)
    e3 = Evento(
        id=re.proximo_id(), sala_id=1, titulo="C", inicio=dt("09:00"), fim=dt("10:00")
    )
    re.adicionar(e3)

    lista = re.listar_por_sala(1)
    assert [e.id for e in lista] == [1, 3]

    # mudar a lista retornada não deve afetar o repositório interno
    lista.append(
        Evento(id=999, sala_id=1, titulo="Z", inicio=dt("10:00"), fim=dt("11:00"))
    )
    # Checa que o estado interno continua com 3 elementos, e listar_por_sala(1) continua [1,3]
    assert [e.id for e in re.listar()] == [1, 2, 3]
    assert [e.id for e in re.listar_por_sala(1)] == [1, 3]
