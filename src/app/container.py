from dataclasses import dataclass

from domínio.repositórios import SalaRepository, EventoRepository
from infra.repos_memória import MemSalaRepository, MemEventoRepository


@dataclass
class Container:
    """Container simples de composição de dependências.

    Fornece instâncias de repositórios para a aplicação. Mantém tudo
    em memória, sem efeitos de I/O externos.
    """

    sala_repo: SalaRepository
    evento_repo: EventoRepository


def criar_container_memoria() -> Container:
    """Cria um container com repositórios em memória independentes."""
    return Container(sala_repo=MemSalaRepository(), evento_repo=MemEventoRepository())
