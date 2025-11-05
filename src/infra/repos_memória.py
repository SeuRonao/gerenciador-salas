from domínio.modelos import Sala, Evento
from domínio.repositórios import SalaRepository, EventoRepository


class MemSalaRepository(SalaRepository):
    """Implementação em memória de SalaRepository.

    Armazena entidades em uma lista interna e provê operações básicas
    de CRUD com id sequencial simples.
    """

    def __init__(self) -> None:
        self._dados: list[Sala] = []

    def proximo_id(self) -> int:
        return (self._dados[-1].id + 1) if self._dados else 1

    def adicionar(self, sala: Sala) -> Sala:
        self._dados.append(sala)
        return sala

    def obter_por_id(self, sala_id: int) -> Sala | None:
        return next((s for s in self._dados if s.id == sala_id), None)

    def listar(self) -> list[Sala]:
        # retorna uma cópia para evitar mutações externas do estado interno
        return list(self._dados)

    def remover(self, sala_id: int) -> bool:
        antes = len(self._dados)
        self._dados = [s for s in self._dados if s.id != sala_id]
        return len(self._dados) < antes

    def atualizar(self, sala: Sala) -> Sala:
        # remove o existente (se houver) e insere o atualizado
        self.remover(sala.id)
        self._dados.append(sala)
        return sala


class MemEventoRepository(EventoRepository):
    """Implementação em memória de EventoRepository."""

    def __init__(self) -> None:
        self._dados: list[Evento] = []

    def proximo_id(self) -> int:
        return (self._dados[-1].id + 1) if self._dados else 1

    def adicionar(self, evento: Evento) -> Evento:
        self._dados.append(evento)
        return evento

    def atualizar(self, evento: Evento) -> Evento:
        self.remover(evento.id)
        self._dados.append(evento)
        return evento

    def remover(self, evento_id: int) -> bool:
        antes = len(self._dados)
        self._dados = [e for e in self._dados if e.id != evento_id]
        return len(self._dados) < antes

    def obter_por_id(self, evento_id: int) -> Evento | None:
        return next((e for e in self._dados if e.id == evento_id), None)

    def listar(self) -> list[Evento]:
        return list(self._dados)

    def listar_por_sala(self, sala_id: int) -> list[Evento]:
        # retorna cópia filtrada para não expor a lista interna
        return [e for e in self._dados if e.sala_id == sala_id]
