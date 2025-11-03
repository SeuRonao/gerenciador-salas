import builtins
from datetime import datetime

import pytest

import main


# Fixture para isolar estado global entre testes
@pytest.fixture(autouse=True)
def reset_estado():
    main.SALAS.clear()
    main.EVENTOS.clear()


def feed_input(monkeypatch, respostas: list[str]):
    it = iter(respostas)
    monkeypatch.setattr(builtins, "input", lambda _="": next(it))


# --- cadastrar_sala ---


def test_cadastrar_sala_sucesso(monkeypatch, capsys):
    feed_input(monkeypatch, ["Sala A", "10"])
    sala = main.cadastrar_sala()
    out = capsys.readouterr().out
    assert sala == {"id": 1, "nome": "Sala A", "capacidade": 10}
    assert main.SALAS == [sala]
    assert "[ok] Sala criada:" in out and "Sala A" in out


def test_cadastrar_sala_nome_vazio(monkeypatch, capsys):
    feed_input(monkeypatch, ["", "999"])  # segunda entrada não deve ser usada
    sala = main.cadastrar_sala()
    out = capsys.readouterr().out
    assert sala is None
    assert main.SALAS == []
    assert "Nome da sala não pode ser vazio" in out


def test_cadastrar_sala_capacidade_invalida_tipo(monkeypatch, capsys):
    feed_input(monkeypatch, ["Sala X", "abc"])
    sala = main.cadastrar_sala()
    out = capsys.readouterr().out
    assert sala is None
    assert "Capacidade deve ser um número inteiro" in out


def test_cadastrar_sala_capacidade_invalida_valor(monkeypatch, capsys):
    feed_input(monkeypatch, ["Sala X", "0"])
    sala = main.cadastrar_sala()
    out = capsys.readouterr().out
    assert sala is None
    assert "Capacidade deve ser maior que zero" in out


# --- remover_sala ---


def test_remover_sala_sem_salas(capsys):
    ok = main.remover_sala()
    out = capsys.readouterr().out
    assert ok is False
    assert "Não há salas cadastradas" in out


def test_remover_sala_id_invalido(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(monkeypatch, ["x"])  # id inválido
    ok = main.remover_sala()
    out = capsys.readouterr().out
    assert ok is False
    assert "id deve ser um número inteiro" in out


def test_remover_sala_nao_encontrada(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(monkeypatch, ["2"])  # não existe
    ok = main.remover_sala()
    out = capsys.readouterr().out
    assert ok is False
    assert "não encontrada" in out


def test_remover_sala_sucesso(monkeypatch, capsys):
    main.SALAS.extend(
        [
            {"id": 1, "nome": "Sala 1", "capacidade": 5},
            {"id": 2, "nome": "Sala 2", "capacidade": 10},
        ]
    )
    feed_input(monkeypatch, ["1"])  # remove a primeira
    ok = main.remover_sala()
    out = capsys.readouterr().out
    assert ok is True
    assert [s["id"] for s in main.SALAS] == [2]
    assert "[ok] Sala removida:" in out


# --- buscar_sala_por_id ---


def test_buscar_sala_sem_salas(capsys):
    sala = main.buscar_sala_por_id()
    out = capsys.readouterr().out
    assert sala is None
    assert "Não há salas cadastradas" in out


def test_buscar_sala_id_invalido(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(monkeypatch, ["x"])  # id inválido
    sala = main.buscar_sala_por_id()
    out = capsys.readouterr().out
    assert sala is None
    assert "id deve ser um número inteiro" in out


def test_buscar_sala_nao_encontrada(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(monkeypatch, ["2"])  # não existe
    sala = main.buscar_sala_por_id()
    out = capsys.readouterr().out
    assert sala is None
    assert "não encontrada" in out


def test_buscar_sala_encontrada(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(monkeypatch, ["1"])  # existe
    sala = main.buscar_sala_por_id()
    out = capsys.readouterr().out
    assert sala == {"id": 1, "nome": "Sala 1", "capacidade": 5}
    assert "Sala encontrada" in out


# --- listar_salas ---


def test_listar_salas_sem_salas(capsys):
    main.listar_salas()
    out = capsys.readouterr().out
    assert "Não há salas cadastradas" in out


def test_listar_salas_com_salas(capsys):
    main.SALAS.extend(
        [
            {"id": 1, "nome": "Sala 1", "capacidade": 5},
            {"id": 2, "nome": "Sala 2", "capacidade": 10},
        ]
    )
    main.listar_salas()
    out = capsys.readouterr().out
    assert "- 1: Sala 1 [5]" in out
    assert "- 2: Sala 2 [10]" in out


# --- criar_evento ---


def test_criar_evento_sem_salas(capsys):
    ev = main.criar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "Cadastre uma sala" in out


def test_criar_evento_sala_id_invalido(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(monkeypatch, ["x"])  # id inválido
    ev = main.criar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "id da sala deve ser um número inteiro" in out


def test_criar_evento_titulo_vazio(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(monkeypatch, ["1", ""])  # título vazio
    ev = main.criar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "título do evento não pode ser vazio" in out


def test_criar_evento_datas_invalidas(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(monkeypatch, ["1", "Reunião", "bad", "bad"])  # datas erradas
    ev = main.criar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "Datas inválidas" in out


def test_criar_evento_sala_nao_existe(monkeypatch, capsys):
    # Sala cadastrada é 1, tentamos 2
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(
        monkeypatch,
        ["2", "Reunião", "2025-10-31 14:30", "2025-10-31 15:30"],
    )
    ev = main.criar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "Sala informada não existe" in out


def test_criar_evento_fim_antes_inicio(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(
        monkeypatch,
        ["1", "Reunião", "2025-10-31 16:30", "2025-10-31 15:30"],
    )
    ev = main.criar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "horário de fim deve ser maior" in out


def test_criar_evento_conflito(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    # Evento existente 14:00-15:00
    main.EVENTOS.append(
        {
            "id": 1,
            "sala_id": 1,
            "titulo": "Existente",
            "inicio": datetime(2025, 10, 31, 14, 0),
            "fim": datetime(2025, 10, 31, 15, 0),
        }
    )
    # Tenta novo em sobreposição 14:30-15:30
    feed_input(
        monkeypatch,
        ["1", "Novo", "2025-10-31 14:30", "2025-10-31 15:30"],
    )
    ev = main.criar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "Conflito de horário" in out


def test_criar_evento_sucesso(monkeypatch, capsys):
    main.SALAS.append({"id": 1, "nome": "Sala 1", "capacidade": 5})
    feed_input(
        monkeypatch,
        ["1", "Reunião", "2025-10-31 14:30", "2025-10-31 15:30"],
    )
    ev = main.criar_evento()
    out = capsys.readouterr().out
    assert ev is not None and ev["id"] == 1 and ev["sala_id"] == 1
    assert isinstance(ev["inicio"], datetime) and isinstance(ev["fim"], datetime)
    assert len(main.EVENTOS) == 1
    assert "[ok] Evento agendado" in out


# --- cancelar_evento ---


def test_cancelar_evento_sem_eventos(capsys):
    ok = main.cancelar_evento()
    out = capsys.readouterr().out
    assert ok is False
    assert "Não há eventos agendados" in out


def test_cancelar_evento_id_invalido(monkeypatch, capsys):
    main.EVENTOS.append(
        {
            "id": 1,
            "sala_id": 1,
            "titulo": "A",
            "inicio": datetime(2025, 1, 1, 10, 0),
            "fim": datetime(2025, 1, 1, 11, 0),
        }
    )
    feed_input(monkeypatch, ["x"])  # inválido
    ok = main.cancelar_evento()
    out = capsys.readouterr().out
    assert ok is False
    assert "id do evento deve ser um número inteiro" in out


def test_cancelar_evento_nao_encontrado(monkeypatch, capsys):
    main.EVENTOS.append(
        {
            "id": 1,
            "sala_id": 1,
            "titulo": "A",
            "inicio": datetime(2025, 1, 1, 10, 0),
            "fim": datetime(2025, 1, 1, 11, 0),
        }
    )
    feed_input(monkeypatch, ["2"])  # não existe
    ok = main.cancelar_evento()
    out = capsys.readouterr().out
    assert ok is False
    assert "não encontrado" in out


def test_cancelar_evento_sucesso(monkeypatch, capsys):
    main.EVENTOS.append(
        {
            "id": 1,
            "sala_id": 1,
            "titulo": "A",
            "inicio": datetime(2025, 1, 1, 10, 0),
            "fim": datetime(2025, 1, 1, 11, 0),
        }
    )
    feed_input(monkeypatch, ["1"])  # cancela
    ok = main.cancelar_evento()
    out = capsys.readouterr().out
    assert ok is True
    assert main.EVENTOS == []
    assert "[ok] Evento cancelado" in out


# --- atualizar_evento ---


def _seed_salas_evento_basico():
    main.SALAS.extend(
        [
            {"id": 1, "nome": "Sala 1", "capacidade": 5},
            {"id": 2, "nome": "Sala 2", "capacidade": 10},
        ]
    )
    main.EVENTOS.append(
        {
            "id": 1,
            "sala_id": 1,
            "titulo": "Evt",
            "inicio": datetime(2025, 1, 1, 10, 0),
            "fim": datetime(2025, 1, 1, 11, 0),
        }
    )


def test_atualizar_evento_sem_eventos(capsys):
    ev = main.atualizar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "Não há eventos para atualizar" in out


def test_atualizar_evento_id_invalido(monkeypatch, capsys):
    _seed_salas_evento_basico()
    feed_input(monkeypatch, ["x"])  # id inválido
    ev = main.atualizar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "id do evento deve ser um número inteiro" in out


def test_atualizar_evento_nao_encontrado(monkeypatch, capsys):
    _seed_salas_evento_basico()
    feed_input(monkeypatch, ["2"])  # não existe
    ev = main.atualizar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "não encontrado" in out


def test_atualizar_evento_manter_campos_em_branco(monkeypatch, capsys):
    _seed_salas_evento_basico()
    # id -> enter -> enter -> enter -> enter
    feed_input(monkeypatch, ["1", "", "", "", ""])
    ev = main.atualizar_evento()
    out = capsys.readouterr().out
    assert ev == {
        "id": 1,
        "sala_id": 1,
        "titulo": "Evt",
        "inicio": datetime(2025, 1, 1, 10, 0),
        "fim": datetime(2025, 1, 1, 11, 0),
    }
    assert "[ok] Evento atualizado" in out


def test_atualizar_evento_sala_inexistente(monkeypatch, capsys):
    _seed_salas_evento_basico()
    feed_input(
        monkeypatch,
        [
            "1",  # escolhe evento
            "Novo título",  # novo título
            "99",  # sala que não existe
            "",  # início mantém
            "",  # fim mantém
        ],
    )
    ev = main.atualizar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "Sala informada não existe" in out


def test_atualizar_evento_datas_invalidas(monkeypatch, capsys):
    _seed_salas_evento_basico()
    feed_input(monkeypatch, ["1", "", "", "bad", "bad"])  # datas inválidas
    ev = main.atualizar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "Datas inválidas" in out


def test_atualizar_evento_fim_antes_inicio(monkeypatch, capsys):
    _seed_salas_evento_basico()
    feed_input(
        monkeypatch,
        [
            "1",
            "",
            "",
            "2025-01-01 12:00",
            "2025-01-01 11:30",  # fim antes
        ],
    )
    ev = main.atualizar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "horário de fim deve ser maior" in out


def test_atualizar_evento_conflito(monkeypatch, capsys):
    _seed_salas_evento_basico()
    # Outro evento na mesma sala 10:30-11:30
    main.EVENTOS.append(
        {
            "id": 2,
            "sala_id": 1,
            "titulo": "Outro",
            "inicio": datetime(2025, 1, 1, 10, 30),
            "fim": datetime(2025, 1, 1, 11, 30),
        }
    )
    # Tenta atualizar o evento 1 para 10:45-11:15 (conflita)
    feed_input(
        monkeypatch,
        [
            "1",
            "",  # título mantém
            "",  # sala mantém (1)
            "2025-01-01 10:45",
            "2025-01-01 11:15",
        ],
    )
    ev = main.atualizar_evento()
    out = capsys.readouterr().out
    assert ev is None
    assert "Conflito de horário" in out


def test_atualizar_evento_sucesso_alterando_tudo(monkeypatch, capsys):
    _seed_salas_evento_basico()
    # Atualiza para sala 2, novo título e novo horário
    feed_input(
        monkeypatch,
        [
            "1",
            "Novo título",
            "2",
            "2025-01-01 09:00",
            "2025-01-01 10:00",
        ],
    )
    ev = main.atualizar_evento()
    out = capsys.readouterr().out
    assert ev is not None
    assert ev["titulo"] == "Novo título"
    assert ev["sala_id"] == 2
    assert ev["inicio"] == datetime(2025, 1, 1, 9, 0)
    assert ev["fim"] == datetime(2025, 1, 1, 10, 0)
    assert "[ok] Evento atualizado" in out


# --- listar_eventos ---


def test_listar_eventos_sem_eventos(capsys):
    main.listar_eventos()
    out = capsys.readouterr().out
    assert "Não há eventos cadastrados" in out


def test_listar_eventos_ordenacao_e_nomes(capsys):
    main.SALAS.extend(
        [
            {"id": 1, "nome": "Sala 1", "capacidade": 5},
            {"id": 2, "nome": "Sala 2", "capacidade": 10},
        ]
    )
    main.EVENTOS.extend(
        [
            {
                "id": 3,
                "sala_id": 2,
                "titulo": "C",
                "inicio": datetime(2025, 1, 1, 10, 0),
                "fim": datetime(2025, 1, 1, 11, 0),
            },
            {
                "id": 1,
                "sala_id": 1,
                "titulo": "A",
                "inicio": datetime(2025, 1, 1, 9, 0),
                "fim": datetime(2025, 1, 1, 10, 0),
            },
            {
                "id": 2,
                "sala_id": 1,
                "titulo": "B",
                "inicio": datetime(2025, 1, 1, 10, 0),
                "fim": datetime(2025, 1, 1, 10, 30),
            },
        ]
    )
    main.listar_eventos()
    out = capsys.readouterr().out
    # Ordem esperada por (inicio, sala_id, id):
    expected_lines = [
        "- 1: A (sala 1 - Sala 1) [2025-01-01 09:00:00 -> 2025-01-01 10:00:00]",
        "- 2: B (sala 1 - Sala 1) [2025-01-01 10:00:00 -> 2025-01-01 10:30:00]",
        "- 3: C (sala 2 - Sala 2) [2025-01-01 10:00:00 -> 2025-01-01 11:00:00]",
    ]
    # Verifica que as três linhas aparecem na ordem
    start = 0
    for line in expected_lines:
        idx = out.find(line, start)
        assert idx != -1, f"Linha esperada não encontrada: {line}\nOut:\n{out}"
        start = idx + 1


# --- menu ---


def test_menu_sai_imediato(monkeypatch, capsys):
    feed_input(monkeypatch, ["0"])  # sair
    main.menu()
    out = capsys.readouterr().out
    assert "Saindo..." in out
