from dataclasses import dataclass
from datetime import datetime


@dataclass
class Sala:
    """Entidade de domínio para Sala.

    Atributos:
    - id: identificador único (inteiro positivo)
    - nome: nome da sala (não vazio)
    - capacidade: número inteiro > 0
    """

    id: int
    nome: str
    capacidade: int

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id da sala deve ser inteiro > 0")
        if not isinstance(self.nome, str) or not self.nome.strip():
            raise ValueError("nome da sala não pode ser vazio")
        if not isinstance(self.capacidade, int) or self.capacidade <= 0:
            raise ValueError("capacidade deve ser inteiro > 0")


@dataclass
class Evento:
    """Entidade de domínio para Evento.

    Atributos:
    - id: identificador do evento (inteiro positivo)
    - sala_id: id da sala existente
    - titulo: título do evento (não vazio)
    - inicio: datetime de início
    - fim: datetime de término (> início)
    """

    id: int
    sala_id: int
    titulo: str
    inicio: datetime
    fim: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id do evento deve ser inteiro > 0")
        if not isinstance(self.sala_id, int) or self.sala_id <= 0:
            raise ValueError("sala_id deve ser inteiro > 0")
        if not isinstance(self.titulo, str) or not self.titulo.strip():
            raise ValueError("título do evento não pode ser vazio")
        if not isinstance(self.inicio, datetime) or not isinstance(self.fim, datetime):
            raise ValueError("inicio e fim devem ser datetime")
        if self.fim <= self.inicio:
            raise ValueError("fim deve ser maior que início")
