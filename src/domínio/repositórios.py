from abc import ABC, abstractmethod

from .modelos import Sala, Evento


class SalaRepository(ABC):
    """Interface abstrata para persistência de salas.

    Implementações concretas podem ser em memória, arquivo ou banco —
    a camada de domínio não deve depender desses detalhes.
    """

    @abstractmethod
    def proximo_id(self) -> int:
        """Retorna o próximo id disponível para uma nova sala."""
        raise NotImplementedError

    @abstractmethod
    def adicionar(self, sala: Sala) -> Sala:
        """Persiste uma nova sala e retorna a entidade persistida."""
        raise NotImplementedError

    @abstractmethod
    def obter_por_id(self, sala_id: int) -> Sala | None:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> list[Sala]:
        raise NotImplementedError

    @abstractmethod
    def remover(self, sala_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def atualizar(self, sala: Sala) -> Sala:
        raise NotImplementedError


class EventoRepository(ABC):
    """Interface abstrata para persistência de eventos."""

    @abstractmethod
    def proximo_id(self) -> int:
        """Retorna o próximo id disponível para um novo evento."""
        raise NotImplementedError

    @abstractmethod
    def adicionar(self, evento: Evento) -> Evento:
        raise NotImplementedError

    @abstractmethod
    def atualizar(self, evento: Evento) -> Evento:
        raise NotImplementedError

    @abstractmethod
    def remover(self, evento_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def obter_por_id(self, evento_id: int) -> Evento | None:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> list[Evento]:
        raise NotImplementedError

    @abstractmethod
    def listar_por_sala(self, sala_id: int) -> list[Evento]:
        raise NotImplementedError
