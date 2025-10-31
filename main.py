from datetime import datetime


SALAS: list[dict] = []
EVENTOS: list[dict] = []


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

    novo_id = (SALAS[-1]["id"] + 1) if SALAS else 1
    sala = {"id": novo_id, "nome": nome, "capacidade": capacidade}
    SALAS.append(sala)
    print("[ok] Sala criada:", sala)
    return sala


def remover_sala() -> bool:
    """
    Remove uma sala por id da variável global SALAS.

    Exibe a lista atual (id - nome [capacidade]) para auxiliar a escolha.
    Retorna True se removeu, False caso contrário.
    """
    if not SALAS:
        print("[aviso] Não há salas cadastradas para remover.")
        return False

    print("=== Remoção de Sala ===")
    print("Salas atuais:")
    for s in SALAS:
        print(f"- {s['id']}: {s['nome']} [{s['capacidade']}]")

    id_str = input("Digite o id da sala a remover: ").strip()
    try:
        alvo = int(id_str)
    except (TypeError, ValueError):
        print("[erro] O id deve ser um número inteiro.")
        return False

    # Procura a sala pelo id
    idx = next((i for i, s in enumerate(SALAS) if s["id"] == alvo), -1)
    if idx == -1:
        print(f"[erro] Sala com id {alvo} não encontrada.")
        return False

    removida = SALAS.pop(idx)
    print("[ok] Sala removida:", removida)
    return True


def buscar_sala_por_id() -> dict | None:
    """Busca uma sala por id em SALAS e imprime o resultado."""
    if not SALAS:
        print("[aviso] Não há salas cadastradas para buscar.")
        return None

    print("=== Buscar Sala por ID ===")
    id_str = input("Digite o id da sala para buscar: ").strip()
    try:
        alvo = int(id_str)
    except (TypeError, ValueError):
        print("[erro] O id deve ser um número inteiro.")
        return None

    sala = next((s for s in SALAS if s["id"] == alvo), None)
    if sala is None:
        print(f"[erro] Sala com id {alvo} não encontrada.")
        return None

    print("[ok] Sala encontrada:", sala)
    return sala


def listar_salas() -> None:
    """Lista todas as salas cadastradas em SALAS."""
    print("=== Listar Salas ===")
    if not SALAS:
        print("[aviso] Não há salas cadastradas.")
        return
    for s in SALAS:
        print(f"- {s['id']}: {s['nome']} [{s['capacidade']}]")


def criar_evento() -> dict | None:
    """Fluxo interativo para criar (agendar) um evento na variável global EVENTOS."""
    if not SALAS:
        print(
            "[aviso] Não há salas cadastradas. Cadastre uma sala antes de agendar eventos."
        )
        return None

    print("=== Agendar Evento ===")
    print("Salas disponíveis:")
    for s in SALAS:
        print(f"- {s['id']}: {s['nome']} [{s['capacidade']}]")

    sala_id_str = input("Digite o id da sala: ").strip()
    try:
        sala_id = int(sala_id_str)
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
    try:
        inicio = datetime.strptime(inicio_str, "%Y-%m-%d %H:%M")
        fim = datetime.strptime(fim_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("[erro] Datas inválidas. Use o formato YYYY-MM-DD HH:MM.")
        return None

    # Validações básicas (agora dentro da função única)
    if not any(s.get("id") == sala_id for s in SALAS):
        print("[erro] Sala informada não existe.")
        return None
    if fim <= inicio:
        print("[erro] O horário de fim deve ser maior que o de início.")
        return None

    # Checa conflitos na mesma sala
    for e in EVENTOS:
        if e.get("sala_id") == sala_id:
            ei = e.get("inicio")
            ef = e.get("fim")
            if not isinstance(ei, datetime) or not isinstance(ef, datetime):
                # Caso dados inesperados, ignore o registro
                continue
            # Conflito se houver sobreposição dos intervalos
            if not (fim <= ei or inicio >= ef):
                print("[erro] Conflito de horário para esta sala.")
                return None

    novo_id = (EVENTOS[-1]["id"] + 1) if EVENTOS else 1
    evento = {
        "id": novo_id,
        "sala_id": sala_id,
        "titulo": titulo,
        "inicio": inicio,
        "fim": fim,
    }
    EVENTOS.append(evento)
    print("[ok] Evento agendado:", evento)
    return evento


def menu():
    """Menu monolítico para escolher operações sobre SALAS."""
    while True:
        print("\n=== Menu ===")
        print("1) Cadastrar sala")
        print("2) Remover sala")
        print("3) Buscar sala por id")
        print("4) Listar salas")
        print("5) Agendar evento")
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
        elif opção == "0":
            print("Saindo...")
            break
        else:
            print("[erro] Opção inválida. Tente novamente.")


def main():
    menu()


if __name__ == "__main__":
    main()
