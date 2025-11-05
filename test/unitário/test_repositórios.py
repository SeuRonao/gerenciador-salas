import pytest

from domínio.repositórios import SalaRepository, EventoRepository


def test_abc_nao_instanciável():
    with pytest.raises(TypeError):
        SalaRepository()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        EventoRepository()  # type: ignore[abstract]


def test_subclasse_minima_pode_instanciar():
    class MemSalaRepo(SalaRepository):
        def __init__(self):
            self._dados = []

        def proximo_id(self) -> int:
            return len(self._dados) + 1

        def adicionar(self, sala):
            self._dados.append(sala)
            return sala

        def obter_por_id(self, sala_id: int):
            return next((s for s in self._dados if s.id == sala_id), None)

        def listar(self):
            return list(self._dados)

        def remover(self, sala_id: int):
            before = len(self._dados)
            self._dados = [s for s in self._dados if s.id != sala_id]
            return len(self._dados) < before

        def atualizar(self, sala):
            self.remover(sala.id)
            self._dados.append(sala)
            return sala

    class MemEventoRepo(EventoRepository):
        def proximo_id(self) -> int:
            return 1

        def adicionar(self, evento):
            return evento

        def atualizar(self, evento):
            return evento

        def remover(self, evento_id: int):
            return False

        def obter_por_id(self, evento_id: int):
            return None

        def listar(self):
            return []

        def listar_por_sala(self, sala_id: int):
            return []

    assert MemSalaRepo() is not None
    assert MemEventoRepo() is not None
