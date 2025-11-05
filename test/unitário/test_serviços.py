from datetime import datetime

from domínio.modelos import Sala, Evento
from domínio.serviços import (
    cadastrar_sala,
    listar_salas,
    remover_sala,
    agendar_evento,
    cancelar_evento,
    atualizar_evento,
    listar_eventos,
)
from domínio.repositórios import SalaRepository, EventoRepository


class MemSalaRepo(SalaRepository):
    def __init__(self) -> None:
        self._dados: list[Sala] = []

    def proximo_id(self) -> int:
        # simples e determinístico para os testes
        return (self._dados[-1].id + 1) if self._dados else 1

    def adicionar(self, sala: Sala) -> Sala:
        self._dados.append(sala)
        return sala

    def obter_por_id(self, sala_id: int) -> Sala | None:
        return next((s for s in self._dados if s.id == sala_id), None)

    def listar(self) -> list[Sala]:
        return list(self._dados)

    def remover(self, sala_id: int) -> bool:
        antes = len(self._dados)
        self._dados = [s for s in self._dados if s.id != sala_id]
        return len(self._dados) < antes

    def atualizar(self, sala: Sala) -> Sala:
        self.remover(sala.id)
        self._dados.append(sala)
        return sala


class MemEventoRepo(EventoRepository):
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
        return [e for e in self._dados if e.sala_id == sala_id]


def dt(hm: str) -> datetime:
    h, m = map(int, hm.split(":"))
    return datetime(2025, 1, 1, h, m)


def test_cadastrar_listar_remover_sala():
    rs = MemSalaRepo()
    assert cadastrar_sala(rs, " ", 10) is None
    assert cadastrar_sala(rs, "Sala 1", 0) is None

    s1 = cadastrar_sala(rs, "Sala 1", 5)
    assert s1 is not None
    _ = cadastrar_sala(rs, "Sala 2", 10)
    assert [s.nome for s in listar_salas(rs)] == ["Sala 1", "Sala 2"]

    assert remover_sala(rs, 999) is False
    assert remover_sala(rs, s1.id) is True
    assert [s.nome for s in listar_salas(rs)] == ["Sala 2"]


def test_agendar_evento_validações_e_sucesso():
    rs = MemSalaRepo()
    re = MemEventoRepo()
    # sem salas
    assert (
        agendar_evento(
            re, rs, sala_id=1, titulo="A", inicio=dt("09:00"), fim=dt("10:00")
        )
        is None
    )

    s = cadastrar_sala(rs, "Sala", 5)
    assert s is not None
    assert (
        agendar_evento(
            re, rs, sala_id=s.id, titulo=" ", inicio=dt("09:00"), fim=dt("10:00")
        )
        is None
    )
    assert (
        agendar_evento(
            re, rs, sala_id=s.id, titulo="A", inicio=dt("10:00"), fim=dt("09:00")
        )
        is None
    )

    e1 = agendar_evento(
        re, rs, sala_id=s.id, titulo="A", inicio=dt("09:00"), fim=dt("10:00")
    )
    assert e1 is not None and e1.id == 1

    # conflito
    assert (
        agendar_evento(
            re, rs, sala_id=s.id, titulo="B", inicio=dt("09:30"), fim=dt("09:45")
        )
        is None
    )

    # outra sala não conflita
    s2 = cadastrar_sala(rs, "Sala 2", 10)
    assert s2 is not None
    e2 = agendar_evento(
        re, rs, sala_id=s2.id, titulo="B", inicio=dt("09:30"), fim=dt("09:45")
    )
    assert e2 is not None and e2.sala_id == s2.id


def test_cancelar_atualizar_e_listar_eventos():
    rs = MemSalaRepo()
    re = MemEventoRepo()
    s1 = cadastrar_sala(rs, "Sala 1", 5)
    s2 = cadastrar_sala(rs, "Sala 2", 10)
    assert s1 is not None and s2 is not None

    # nada para atualizar/cancelar
    assert cancelar_evento(re, 1) is False
    assert atualizar_evento(re, rs, 1, titulo="X") is None

    e = agendar_evento(
        re, rs, sala_id=s1.id, titulo="A", inicio=dt("09:00"), fim=dt("10:00")
    )
    assert e is not None

    # validações atualização
    assert atualizar_evento(re, rs, e.id, titulo=" ") is None
    assert atualizar_evento(re, rs, e.id, sala_id=999) is None
    assert atualizar_evento(re, rs, e.id, inicio=dt("10:00"), fim=dt("09:00")) is None

    # cria um evento que NÃO conflita inicialmente (borda 10:00-10:30),
    # mas passará a conflitar após a tentativa de atualização
    _ = agendar_evento(
        re, rs, sala_id=s1.id, titulo="B", inicio=dt("10:00"), fim=dt("10:30")
    )
    assert atualizar_evento(re, rs, e.id, inicio=dt("09:45"), fim=dt("10:15")) is None

    # sucesso alterando tudo, inclusive sala
    e2 = atualizar_evento(
        re,
        rs,
        e.id,
        titulo="Novo",
        sala_id=s2.id,
        inicio=dt("08:00"),
        fim=dt("09:00"),
    )
    assert (
        e2 is not None
        and e2.titulo == "Novo"
        and e2.sala_id == s2.id
        and e2.inicio == dt("08:00")
    )

    # cancelar
    assert cancelar_evento(re, e2.id) is True

    # listar ordenado
    e3 = agendar_evento(
        re, rs, sala_id=s1.id, titulo="X", inicio=dt("07:00"), fim=dt("08:00")
    )
    e4 = agendar_evento(
        re, rs, sala_id=s2.id, titulo="Y", inicio=dt("07:00"), fim=dt("08:00")
    )
    e5 = agendar_evento(
        re, rs, sala_id=s1.id, titulo="Z", inicio=dt("09:00"), fim=dt("10:00")
    )
    ordenados = listar_eventos(re)
    assert e3 is not None and e4 is not None and e5 is not None
    ids = [e.id for e in ordenados]
    # Os três primeiros devem ser e3, e4 (mesmo horário, ordena por sala_id), depois e5
    assert ids[:3] == [e3.id, e4.id, e5.id]
