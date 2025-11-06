from datetime import datetime

# Integração incremental com a camada de domínio (DDD)
# Para iniciar a migração mantendo compatibilidade com os testes E2E
# (que dependem das listas globais SALAS/EVENTOS), o cadastro de sala
# passará a usar o serviço de domínio através de um repositório "adapter"
# que escreve/consulta diretamente nessas listas globais.
from domínio.modelos import Sala as _Sala
from domínio.repositórios import SalaRepository as _SalaRepository
from domínio.serviços import cadastrar_sala as _srv_cadastrar_sala


SALAS: list[dict] = []
EVENTOS: list[dict] = []


class _SalaRepoDoMain(_SalaRepository):
    """Adapter de repositório que persiste nas listas globais do main.

    Objetivo: permitir usar os serviços do domínio sem quebrar os testes
    existentes que verificam `main.SALAS` diretamente.
    """

    def proximo_id(self) -> int:
        return (SALAS[-1]["id"] + 1) if SALAS else 1

    def adicionar(self, sala: _Sala) -> _Sala:
        SALAS.append({"id": sala.id, "nome": sala.nome, "capacidade": sala.capacidade})
        return sala

    def obter_por_id(self, sala_id: int) -> _Sala | None:
        s = next((s for s in SALAS if s["id"] == sala_id), None)
        if s is None:
            return None
        return _Sala(id=s["id"], nome=s["nome"], capacidade=s["capacidade"])

    def listar(self) -> list[_Sala]:
        return [
            _Sala(id=s["id"], nome=s["nome"], capacidade=s["capacidade"]) for s in SALAS
        ]

    def remover(self, sala_id: int) -> bool:
        antes = len(SALAS)
        # mantém comportamento do main (opera em dicts)
        restantes = [s for s in SALAS if s["id"] != sala_id]
        SALAS.clear()
        SALAS.extend(restantes)
        return len(SALAS) < antes

    def atualizar(self, sala: _Sala) -> _Sala:
        self.remover(sala.id)
        self.adicionar(sala)
        return sala


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

    # Agora usamos o serviço de domínio, mas preservamos o estado em SALAS
    # por meio do adaptador `_SalaRepoDoMain`.
    repo = _SalaRepoDoMain()
    criada = _srv_cadastrar_sala(repo, nome, capacidade)
    if criada is None:
        # Em teoria, não deve ocorrer pois já validamos entrada; fallback seguro.
        print("[erro] Dados inválidos para cadastro da sala.")
        return None

    sala = {"id": criada.id, "nome": criada.nome, "capacidade": criada.capacidade}
    # O repo já inseriu em SALAS; garantimos retorno/print no formato antigo
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


def cancelar_evento() -> bool:
    """Remove um evento por id da variável global EVENTOS."""
    if not EVENTOS:
        print("[aviso] Não há eventos agendados para cancelar.")
        return False

    print("=== Cancelar Evento ===")
    print("Eventos atuais:")
    for e in EVENTOS:
        ini = e.get("inicio")
        fim = e.get("fim")
        print(f"- {e['id']}: {e['titulo']} (sala {e['sala_id']}) [{ini} -> {fim}]")

    id_str = input("Digite o id do evento a cancelar: ").strip()
    try:
        alvo = int(id_str)
    except (TypeError, ValueError):
        print("[erro] O id do evento deve ser um número inteiro.")
        return False

    idx = next((i for i, e in enumerate(EVENTOS) if e.get("id") == alvo), -1)
    if idx == -1:
        print(f"[erro] Evento com id {alvo} não encontrado.")
        return False

    removido = EVENTOS.pop(idx)
    print("[ok] Evento cancelado:", removido)
    return True


def atualizar_evento() -> dict | None:
    """Atualiza campos de um evento existente (título, sala, início, fim)."""
    if not EVENTOS:
        print("[aviso] Não há eventos para atualizar.")
        return None

    print("=== Atualizar Evento ===")
    print("Eventos atuais:")
    for e in EVENTOS:
        ini = e.get("inicio")
        fim = e.get("fim")
        print(f"- {e['id']}: {e['titulo']} (sala {e['sala_id']}) [{ini} -> {fim}]")

    id_str = input("Digite o id do evento a atualizar: ").strip()
    try:
        alvo = int(id_str)
    except (TypeError, ValueError):
        print("[erro] O id do evento deve ser um número inteiro.")
        return None

    ev = next((e for e in EVENTOS if e.get("id") == alvo), None)
    if ev is None:
        print(f"[erro] Evento com id {alvo} não encontrado.")
        return None

    print("Deixe em branco para manter o valor atual.")
    novo_titulo = input(f"Título [{ev['titulo']}]: ").strip()
    if not novo_titulo:
        novo_titulo = ev["titulo"]

    print("Salas disponíveis:")
    for s in SALAS:
        print(f"- {s['id']}: {s['nome']} [{s['capacidade']}]")
    sala_in_str = input(f"Sala id [{ev['sala_id']}]: ").strip()
    if sala_in_str:
        try:
            novo_sala_id = int(sala_in_str)
        except (TypeError, ValueError):
            print("[erro] O id da sala deve ser um número inteiro.")
            return None
    else:
        novo_sala_id = ev["sala_id"]

    print("Formato de data/hora: YYYY-MM-DD HH:MM")
    ini_in = input(f"Início [{ev['inicio']}]: ").strip()
    fim_in = input(f"Fim [{ev['fim']}]: ").strip()
    try:
        novo_inicio = (
            datetime.strptime(ini_in, "%Y-%m-%d %H:%M") if ini_in else ev["inicio"]
        )
        novo_fim = datetime.strptime(fim_in, "%Y-%m-%d %H:%M") if fim_in else ev["fim"]
    except ValueError:
        print("[erro] Datas inválidas. Use o formato YYYY-MM-DD HH:MM.")
        return None

    # Validações
    if not any(s.get("id") == novo_sala_id for s in SALAS):
        print("[erro] Sala informada não existe.")
        return None
    if not novo_titulo:
        print("[erro] O título do evento não pode ser vazio.")
        return None
    if novo_fim <= novo_inicio:
        print("[erro] O horário de fim deve ser maior que o de início.")
        return None

    # Conflitos (ignora o próprio evento)
    for e in EVENTOS:
        if e.get("id") == ev["id"]:
            continue
        if e.get("sala_id") == novo_sala_id:
            ei = e.get("inicio")
            ef = e.get("fim")
            if not isinstance(ei, datetime) or not isinstance(ef, datetime):
                continue
            if not (novo_fim <= ei or novo_inicio >= ef):
                print("[erro] Conflito de horário para esta sala.")
                return None

    # Persistir alterações
    ev["titulo"] = novo_titulo
    ev["sala_id"] = novo_sala_id
    ev["inicio"] = novo_inicio
    ev["fim"] = novo_fim

    print("[ok] Evento atualizado:", ev)
    return ev


def listar_eventos() -> None:
    """Lista todos os eventos cadastrados."""
    print("=== Listar Eventos ===")
    if not EVENTOS:
        print("[aviso] Não há eventos cadastrados.")
        return

    # Mapa auxiliar de sala_id -> nome
    mapa_salas = {s.get("id"): s.get("nome") for s in SALAS}
    # Ordena por início, depois sala_id e id
    ordenados = sorted(
        EVENTOS,
        key=lambda e: (
            e.get("inicio"),
            e.get("sala_id"),
            e.get("id"),
        ),
    )
    for e in ordenados:
        sid = e.get("sala_id")
        snome = mapa_salas.get(sid, "(desconhecida)")
        ini = e.get("inicio")
        fim = e.get("fim")
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
