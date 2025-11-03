"""Camada de domínio do Gerenciador de Salas.

Contém:
- modelos (dataclasses para Sala e Evento)
- regras (funções puras de validação e checagem de conflitos)
- repositórios (interfaces abstratas para persistência)
- serviços (funções de caso de uso que usam repos e regras, sem I/O)

Observação: mantenha esta camada livre de prints/input e de qualquer
acoplamento a UI/CLI. Ela deve ser facilmente testável.
"""

from .modelos import Sala, Evento

__all__ = ["Sala", "Evento"]
