from datetime import datetime

from domínio.modelos import Sala, Evento
from infra.repos_memória import MemSalaRepository, MemEventoRepository

from app.container import criar_container_memória  # type: ignore


def dt(hm: str) -> datetime:
    h, m = map(int, hm.split(":"))
    return datetime(2025, 1, 1, h, m)


def test_criar_container_memoria_tipos():
    c = criar_container_memória()
    assert isinstance(c.sala_repo, MemSalaRepository)
    assert isinstance(c.evento_repo, MemEventoRepository)


def test_containers_isolados_por_instancia():
    c1 = criar_container_memória()
    c2 = criar_container_memória()

    s1 = Sala(id=c1.sala_repo.proximo_id(), nome="S1", capacidade=5)
    c1.sala_repo.adicionar(s1)

    # c2 deve continuar vazio
    assert c2.sala_repo.obter_por_id(s1.id) is None
    assert c2.sala_repo.listar() == []


def test_proximo_id_determinístico_por_container():
    c = criar_container_memória()

    assert c.sala_repo.proximo_id() == 1
    c.sala_repo.adicionar(Sala(id=1, nome="S1", capacidade=5))
    assert c.sala_repo.proximo_id() == 2

    assert c.evento_repo.proximo_id() == 1
    c.evento_repo.adicionar(
        Evento(id=1, sala_id=1, titulo="A", inicio=dt("09:00"), fim=dt("10:00"))
    )
    assert c.evento_repo.proximo_id() == 2
