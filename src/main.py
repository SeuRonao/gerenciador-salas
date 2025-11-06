from datetime import datetime

# Integração com a camada de domínio (DDD), agora sem variáveis globais de dados.
from domínio.repositórios import (
    SalaRepository as _SalaRepository,
    EventoRepository as _EventoRepository,
)
from app.container import criar_container_memória as _criar_container_memória
from app import fachada as _fachada

# Container de repositórios em memória. Ao recarregar o módulo (usado nos testes),
# o estado é isolado automaticamente, substituindo as antigas listas globais.
_container = _criar_container_memória()


def cadastrar_sala() -> dict | None:
    """Realiza input/print e cadastra uma sala na variável global SALAS."""

    print("=== Cadastro de Sala ===")
    nome = input("Nome da sala: ").strip()
    if not nome:
        print("[erro] Nome da sala não pode ser vazio.")
        return None

    cap_str = input("Capacidade (inteiro > 0): ").strip()
    try:
        capacidade = int(cap_str)
    except (TypeError, ValueError):
        print("[erro] Capacidade deve ser um número inteiro.")
        return None

    if capacidade <= 0:
        print("[erro] Capacidade deve ser maior que zero.")
        return None

    # Encaminha via fachada (UI -> domínio), preservando mensagens/retorno
    ok, result = _fachada.cadastrar_sala_ui(_container, nome, str(capacidade))
    if not ok:
        print("[erro] Dados inválidos para cadastro da sala.")
        return None

    criada = result  # entidade de domínio Sala
    sala = {"id": criada.id, "nome": criada.nome, "capacidade": criada.capacidade}
    print("[ok] Sala criada:", sala)
    return sala


def remover_sala() -> bool:
    """
    Remove uma sala por id da variável global SALAS.

    Exibe a lista atual (id - nome [capacidade]) para auxiliar a escolha.
    Retorna True se removeu, False caso contrário.
    """
    repo: _SalaRepository = _container.sala_repo
    if not repo.listar():
        print("[aviso] Não há salas cadastradas para remover.")
        return False

    print("=== Remoção de Sala ===")
    print("Salas atuais:")
    for s in repo.listar():
        print(f"- {s.id}: {s.nome} [{s.capacidade}]")

    id_str = input("Digite o id da sala a remover: ").strip()
    # Procura a sala antes para imprimir se remoção for bem-sucedida
    alvo_int = None
    try:
        alvo_int = int(id_str)
    except (TypeError, ValueError):
        pass
    s = repo.obter_por_id(alvo_int) if isinstance(alvo_int, int) else None

    ok, result = _fachada.remover_sala_ui(_container, id_str)
    if not ok:
        msg = str(result)
        if msg == "id da sala inválido":
            print("[erro] O id deve ser um número inteiro.")
        else:
            # tenta usar o valor numérico se possível para manter a mensagem
            try:
                alvo_num = int(id_str)
            except Exception:
                alvo_num = id_str
            print(f"[erro] Sala com id {alvo_num} não encontrada.")
        return False

    removida = (
        {"id": s.id, "nome": s.nome, "capacidade": s.capacidade}
        if s is not None
        else {"id": int(id_str)}
    )
    print("[ok] Sala removida:", removida)
    return True


def buscar_sala_por_id() -> dict | None:
    """Busca uma sala por id em SALAS e imprime o resultado."""
    repo: _SalaRepository = _container.sala_repo
    if not repo.listar():
        print("[aviso] Não há salas cadastradas para buscar.")
        return None

    print("=== Buscar Sala por ID ===")
    id_str = input("Digite o id da sala para buscar: ").strip()
    ok, result = _fachada.buscar_sala_por_id_ui(_container, id_str)
    if not ok:
        msg = str(result)
        if msg == "id da sala inválido":
            print("[erro] O id deve ser um número inteiro.")
        else:
            # para a mensagem, tenta normalizar para inteiro
            try:
                alvo_num = int(id_str)
            except Exception:
                alvo_num = id_str
            print(f"[erro] Sala com id {alvo_num} não encontrada.")
        return None

    s = result
    sala_dict = {"id": s.id, "nome": s.nome, "capacidade": s.capacidade}
    print("[ok] Sala encontrada:", sala_dict)
    return sala_dict


def listar_salas() -> None:
    """Lista todas as salas cadastradas em SALAS."""
    print("=== Listar Salas ===")
    itens = _fachada.listar_salas_ui(_container)
    if not itens:
        print("[aviso] Não há salas cadastradas.")
        return
    for s in itens:
        print(f"- {s['id']}: {s['nome']} [{s['capacidade']}]")


def criar_evento() -> dict | None:
    """Fluxo interativo para criar (agendar) um evento na variável global EVENTOS."""
    repo_salas: _SalaRepository = _container.sala_repo
    if not repo_salas.listar():
        print(
            "[aviso] Não há salas cadastradas. Cadastre uma sala antes de agendar eventos."
        )
        return None

    print("=== Agendar Evento ===")
    print("Salas disponíveis:")
    for s in repo_salas.listar():
        print(f"- {s.id}: {s.nome} [{s.capacidade}]")

    sala_id_str = input("Digite o id da sala: ").strip()
    # Validação antecipada para manter sequência de prompts dos testes
    try:
        int(sala_id_str)
    except (TypeError, ValueError):
        print("[erro] O id da sala deve ser um número inteiro.")
        return None

    titulo = input("Título do evento: ").strip()
    if not titulo:
        print("[erro] O título do evento não pode ser vazio.")
        return None

    print("Formato de data/hora: YYYY-MM-DD HH:MM (ex.: 2025-10-31 14:30)")
    inicio_str = input("Início: ").strip()
    fim_str = input("Fim: ").strip()
    # Validação de parsing de datas para manter mensagens
    try:
        datetime.strptime(inicio_str, "%Y-%m-%d %H:%M")
        datetime.strptime(fim_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("[erro] Datas inválidas. Use o formato YYYY-MM-DD HH:MM.")
        return None

    ok, result = _fachada.agendar_evento_ui(
        _container, sala_id_str, titulo, inicio_str, fim_str
    )
    if not ok:
        msg = str(result)
        # Mapeia mensagens da fachada para as mensagens legadas do main
        if msg == "id da sala inválido":
            print("[erro] O id da sala deve ser um número inteiro.")
        elif msg.startswith("formato de data inválido"):
            print("[erro] Datas inválidas. Use o formato YYYY-MM-DD HH:MM.")
        elif msg == "sala não existe":
            print("[erro] Sala informada não existe.")
        elif msg == "título inválido":
            print("[erro] O título do evento não pode ser vazio.")
        elif msg == "intervalo de datas inválido":
            print("[erro] O horário de fim deve ser maior que o de início.")
        elif msg == "conflito de horário":
            print("[erro] Conflito de horário para esta sala.")
        else:
            print("[erro] Não foi possível agendar o evento.")
        return None

    ev = result
    evento = {
        "id": ev.id,
        "sala_id": ev.sala_id,
        "titulo": ev.titulo,
        "inicio": ev.inicio,
        "fim": ev.fim,
    }
    print("[ok] Evento agendado:", evento)
    return evento


def cancelar_evento() -> bool:
    """Remove um evento por id da variável global EVENTOS."""
    repo_eventos: _EventoRepository = _container.evento_repo
    if not repo_eventos.listar():
        print("[aviso] Não há eventos agendados para cancelar.")
        return False

    print("=== Cancelar Evento ===")
    print("Eventos atuais:")
    for e in repo_eventos.listar():
        ini = e.inicio
        fim = e.fim
        print(f"- {e.id}: {e.titulo} (sala {e.sala_id}) [{ini} -> {fim}]")

    id_str = input("Digite o id do evento a cancelar: ").strip()
    # Captura o evento para impressão caso a remoção ocorra (se id válido)
    alvo = None
    try:
        alvo = int(id_str)
    except (TypeError, ValueError):
        pass
    e = repo_eventos.obter_por_id(alvo) if isinstance(alvo, int) else None

    ok, result = _fachada.cancelar_evento_ui(_container, id_str)
    if not ok:
        msg = str(result)
        if msg == "id do evento inválido":
            print("[erro] O id do evento deve ser um número inteiro.")
        else:
            print(f"[erro] Evento com id {id_str} não encontrado.")
        return False

    removido = (
        {
            "id": e.id,
            "sala_id": e.sala_id,
            "titulo": e.titulo,
            "inicio": e.inicio,
            "fim": e.fim,
        }
        if e is not None
        else {"id": int(id_str)}
    )
    print("[ok] Evento cancelado:", removido)
    return True


def atualizar_evento() -> dict | None:
    """Atualiza campos de um evento existente (título, sala, início, fim)."""
    repo_eventos: _EventoRepository = _container.evento_repo
    repo_salas: _SalaRepository = _container.sala_repo
    if not repo_eventos.listar():
        print("[aviso] Não há eventos para atualizar.")
        return None

    print("=== Atualizar Evento ===")
    print("Eventos atuais:")
    for e in repo_eventos.listar():
        ini = e.inicio
        fim = e.fim
        print(f"- {e.id}: {e.titulo} (sala {e.sala_id}) [{ini} -> {fim}]")

    id_str = input("Digite o id do evento a atualizar: ").strip()
    try:
        alvo = int(id_str)
    except (TypeError, ValueError):
        print("[erro] O id do evento deve ser um número inteiro.")
        return None

    ev = repo_eventos.obter_por_id(alvo)
    if ev is None:
        print(f"[erro] Evento com id {alvo} não encontrado.")
        return None

    print("Deixe em branco para manter o valor atual.")
    novo_titulo = input(f"Título [{ev.titulo}]: ").strip()
    if not novo_titulo:
        novo_titulo = ev.titulo

    print("Salas disponíveis:")
    for s in repo_salas.listar():
        print(f"- {s.id}: {s.nome} [{s.capacidade}]")
    sala_in_str = input(f"Sala id [{ev.sala_id}]: ").strip()
    if sala_in_str:
        try:
            novo_sala_id = int(sala_in_str)
        except (TypeError, ValueError):
            print("[erro] O id da sala deve ser um número inteiro.")
            return None
    else:
        novo_sala_id = ev.sala_id

    print("Formato de data/hora: YYYY-MM-DD HH:MM")
    ini_in = input(f"Início [{ev.inicio}]: ").strip()
    fim_in = input(f"Fim [{ev.fim}]: ").strip()
    try:
        novo_inicio = (
            datetime.strptime(ini_in, "%Y-%m-%d %H:%M") if ini_in else ev.inicio
        )
        novo_fim = datetime.strptime(fim_in, "%Y-%m-%d %H:%M") if fim_in else ev.fim
    except ValueError:
        print("[erro] Datas inválidas. Use o formato YYYY-MM-DD HH:MM.")
        return None

    # Validações
    if repo_salas.obter_por_id(novo_sala_id) is None:
        print("[erro] Sala informada não existe.")
        return None
    if not novo_titulo:
        print("[erro] O título do evento não pode ser vazio.")
        return None
    if novo_fim <= novo_inicio:
        print("[erro] O horário de fim deve ser maior que o de início.")
        return None

    # Conflitos (ignora o próprio evento)
    for e2 in repo_eventos.listar_por_sala(novo_sala_id):
        if e2.id == ev.id:
            continue
        ei = e2.inicio
        ef = e2.fim
        if not (novo_fim <= ei or novo_inicio >= ef):
            print("[erro] Conflito de horário para esta sala.")
            return None

    # Persistir alterações via serviço de domínio e adaptadores
    from domínio.serviços import atualizar_evento as _srv_atualizar_evento

    atualizado = _srv_atualizar_evento(
        repo_eventos,
        repo_salas,
        ev.id,
        titulo=novo_titulo,
        sala_id=novo_sala_id,
        inicio=novo_inicio,
        fim=novo_fim,
    )
    if atualizado is None:
        # Fallback: caso alguma validação do serviço falhe (não esperado aqui)
        print("[erro] Não foi possível atualizar o evento.")
        return None

    ev_dict = {
        "id": atualizado.id,
        "sala_id": atualizado.sala_id,
        "titulo": atualizado.titulo,
        "inicio": atualizado.inicio,
        "fim": atualizado.fim,
    }

    print("[ok] Evento atualizado:", ev_dict)
    return ev_dict


def listar_eventos() -> None:
    """Lista todos os eventos cadastrados."""
    print("=== Listar Eventos ===")
    repo_salas: _SalaRepository = _container.sala_repo
    itens = _fachada.listar_eventos_ui(_container)
    if not itens:
        print("[aviso] Não há eventos cadastrados.")
        return

    # Mantém a impressão anterior incluindo o nome da sala
    mapa_salas = {s.id: s.nome for s in repo_salas.listar()}
    for e in itens:
        sid = e["sala_id"]
        snome = mapa_salas.get(sid, "(desconhecida)")
        ini = e["inicio"]
        fim = e["fim"]
        print(f"- {e['id']}: {e['titulo']} (sala {sid} - {snome}) [{ini} -> {fim}]")


def menu():
    """Menu monolítico para escolher operações sobre SALAS."""
    while True:
        print("\n=== Menu ===")
        print("1) Cadastrar sala")
        print("2) Remover sala")
        print("3) Buscar sala por id")
        print("4) Listar salas")
        print("5) Agendar evento")
        print("6) Cancelar evento")
        print("7) Atualizar evento")
        print("8) Listar eventos")
        print("0) Sair")
        opção = input("Escolha uma opção: ").strip()

        if opção == "1":
            cadastrar_sala()
        elif opção == "2":
            remover_sala()
        elif opção == "3":
            buscar_sala_por_id()
        elif opção == "4":
            listar_salas()
        elif opção == "5":
            criar_evento()
        elif opção == "6":
            cancelar_evento()
        elif opção == "7":
            atualizar_evento()
        elif opção == "8":
            listar_eventos()
        elif opção == "0":
            print("Saindo...")
            break
        else:
            print("[erro] Opção inválida. Tente novamente.")


def main():
    menu()


if __name__ == "__main__":
    main()
