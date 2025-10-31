SALAS: list[dict] = []


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


def main():
    cadastrar_sala()


if __name__ == "__main__":
    main()
