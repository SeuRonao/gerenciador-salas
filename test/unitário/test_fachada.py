from datetime import datetime

from domínio.modelos import Sala, Evento

# testes TDD: o módulo app.fachada não existe ainda e os imports devem falhar
from app import fachada  # type: ignore


def dt(hm: str) -> datetime:
    h, m = map(int, hm.split(":"))
    return datetime(2025, 1, 1, h, m)


def test_cadastrar_sala_ui_sucesso(container_memoria):
    c = container_memoria

    ok, resultado = fachada.cadastrar_sala_ui(c, "Sala X", "10")
    assert ok is True
    assert isinstance(resultado, Sala)
    assert c.sala_repo.obter_por_id(resultado.id) is resultado


def test_cadastrar_sala_ui_capacidade_invalida(container_memoria):
    c = container_memoria

    ok, erro = fachada.cadastrar_sala_ui(c, "Sala X", "abc")
    assert ok is False
    assert "capacidade" in erro.lower()


def test_agendar_evento_ui_sucesso(container_memoria):
    c = container_memoria
    # cria sala direto no repo para simplificar
    s = Sala(id=c.sala_repo.proximo_id(), nome="Sala 1", capacidade=5)
    c.sala_repo.adicionar(s)

    ok, resultado = fachada.agendar_evento_ui(
        c, str(s.id), "Reunião", "2025-01-01 09:00", "2025-01-01 10:00"
    )
    assert ok is True
    assert isinstance(resultado, Evento)
    assert c.evento_repo.obter_por_id(resultado.id) is resultado


def test_agendar_evento_ui_conflito(container_memoria):
    c = container_memoria
    s = Sala(id=c.sala_repo.proximo_id(), nome="Sala 1", capacidade=5)
    c.sala_repo.adicionar(s)

    # adiciona evento existente 09:00-10:00
    e = Evento(
        id=c.evento_repo.proximo_id(),
        sala_id=s.id,
        titulo="Existente",
        inicio=dt("09:00"),
        fim=dt("10:00"),
    )
    c.evento_repo.adicionar(e)

    ok, erro = fachada.agendar_evento_ui(
        c, str(s.id), "Novo", "2025-01-01 09:30", "2025-01-01 10:30"
    )
    assert ok is False
    assert "conflito" in erro.lower()


def test_cancelar_evento_ui_sucesso_e_nao_encontrado(container_memoria):
    c = container_memoria
    s = Sala(id=c.sala_repo.proximo_id(), nome="Sala 1", capacidade=5)
    c.sala_repo.adicionar(s)

    e = Evento(
        id=c.evento_repo.proximo_id(),
        sala_id=s.id,
        titulo="Evt",
        inicio=dt("09:00"),
        fim=dt("10:00"),
    )
    c.evento_repo.adicionar(e)

    ok, msg = fachada.cancelar_evento_ui(c, str(e.id))
    assert ok is True
    assert msg is None
    # cancelar novamente
    ok2, msg2 = fachada.cancelar_evento_ui(c, str(e.id))
    assert ok2 is False
    assert "não encontrado" in msg2.lower()


def test_atualizar_evento_ui_datas_invalidas(container_memoria):
    c = container_memoria
    s = Sala(id=c.sala_repo.proximo_id(), nome="Sala 1", capacidade=5)
    c.sala_repo.adicionar(s)

    e = Evento(
        id=c.evento_repo.proximo_id(),
        sala_id=s.id,
        titulo="Evt",
        inicio=dt("09:00"),
        fim=dt("10:00"),
    )
    c.evento_repo.adicionar(e)

    ok, erro = fachada.atualizar_evento_ui(
        c, str(e.id), titulo=None, sala_id=None, inicio="bad", fim="bad"
    )
    assert ok is False
    assert "data" in erro.lower() or "formato" in erro.lower()


def test_listar_salas_eventos_ui_retorna_estruturas_simples(container_memoria):
    c = container_memoria
    s = Sala(id=c.sala_repo.proximo_id(), nome="Sala 1", capacidade=5)
    c.sala_repo.adicionar(s)
    e = Evento(
        id=c.evento_repo.proximo_id(),
        sala_id=s.id,
        titulo="Evt",
        inicio=dt("07:00"),
        fim=dt("08:00"),
    )
    c.evento_repo.adicionar(e)

    salas = fachada.listar_salas_ui(c)
    eventos = fachada.listar_eventos_ui(c)

    assert isinstance(salas, list)
    assert isinstance(eventos, list)
    assert any(isinstance(x, dict) and x.get("nome") == "Sala 1" for x in salas)
    assert any(isinstance(x, dict) and x.get("titulo") == "Evt" for x in eventos)
