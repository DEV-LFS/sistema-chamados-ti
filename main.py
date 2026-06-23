import sqlite3
from pathlib import Path


CAMINHO_BANCO = Path(__file__).resolve().parent / "chamados.db"


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    # Permite acessar os dados usando o nome das colunas.
    conexao.row_factory = sqlite3.Row

    return conexao


def criar_tabela():
    with conectar_banco() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS chamados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Aberto',
                data_criacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def ler_id(mensagem):
    valor = input(mensagem).strip()

    try:
        id_chamado = int(valor)

        if id_chamado <= 0:
            print("\nErro: o ID precisa ser maior que zero.")
            return None

        return id_chamado

    except ValueError:
        print("\nErro: informe um ID numérico.")
        return None


def exibir_chamado(chamado):
    print(f"\nID: {chamado['id']}")
    print(f"Título: {chamado['titulo']}")
    print(f"Descrição: {chamado['descricao']}")
    print(f"Categoria: {chamado['categoria']}")
    print(f"Prioridade: {chamado['prioridade']}")
    print(f"Status: {chamado['status']}")
    print(f"Data de criação: {chamado['data_criacao']}")
    print("-" * 40)


def criar_chamado():
    print("\n--- ABRIR NOVO CHAMADO ---")

    titulo = input("Título do problema: ").strip()
    descricao = input("Descrição do problema: ").strip()
    categoria = input("Categoria: ").strip()
    prioridade = input("Prioridade (Baixa, Média ou Alta): ").strip()

    if not titulo or not descricao or not categoria or not prioridade:
        print("\nErro: todos os campos são obrigatórios.")
        return

    with conectar_banco() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO chamados (
                titulo,
                descricao,
                categoria,
                prioridade,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                titulo,
                descricao,
                categoria,
                prioridade,
                "Aberto"
            )
        )

        id_chamado = cursor.lastrowid

    print(f"\nChamado {id_chamado} criado com sucesso!")


def listar_chamados():
    print("\n--- LISTA DE CHAMADOS ---")

    with conectar_banco() as conexao:
        chamados = conexao.execute(
            """
            SELECT
                id,
                titulo,
                descricao,
                categoria,
                prioridade,
                status,
                data_criacao
            FROM chamados
            ORDER BY id
            """
        ).fetchall()

    if not chamados:
        print("Nenhum chamado cadastrado.")
        return

    for chamado in chamados:
        exibir_chamado(chamado)


def buscar_chamado():
    print("\n--- BUSCAR CHAMADO ---")

    id_chamado = ler_id("Informe o ID do chamado: ")

    if id_chamado is None:
        return

    with conectar_banco() as conexao:
        chamado = conexao.execute(
            """
            SELECT
                id,
                titulo,
                descricao,
                categoria,
                prioridade,
                status,
                data_criacao
            FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        ).fetchone()

    if chamado is None:
        print(f"\nChamado com ID {id_chamado} não encontrado.")
        return

    exibir_chamado(chamado)


def atualizar_status():
    print("\n--- ATUALIZAR STATUS ---")

    id_chamado = ler_id("Informe o ID do chamado: ")

    if id_chamado is None:
        return

    with conectar_banco() as conexao:
        chamado = conexao.execute(
            """
            SELECT id, titulo, status
            FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        ).fetchone()

    if chamado is None:
        print(f"\nChamado com ID {id_chamado} não encontrado.")
        return

    print(f"\nChamado: {chamado['titulo']}")
    print(f"Status atual: {chamado['status']}")
    print("\n1 - Aberto")
    print("2 - Em andamento")
    print("3 - Resolvido")
    print("4 - Fechado")

    opcao = input("Escolha o novo status: ").strip()

    status_disponiveis = {
        "1": "Aberto",
        "2": "Em andamento",
        "3": "Resolvido",
        "4": "Fechado"
    }

    novo_status = status_disponiveis.get(opcao)

    if novo_status is None:
        print("\nOpção de status inválida.")
        return

    with conectar_banco() as conexao:
        conexao.execute(
            """
            UPDATE chamados
            SET status = ?
            WHERE id = ?
            """,
            (novo_status, id_chamado)
        )

    print(
        f"\nStatus do chamado {id_chamado} "
        f"atualizado para '{novo_status}'."
    )


def excluir_chamado():
    print("\n--- EXCLUIR CHAMADO ---")

    id_chamado = ler_id("Informe o ID do chamado: ")

    if id_chamado is None:
        return

    with conectar_banco() as conexao:
        chamado = conexao.execute(
            """
            SELECT id, titulo
            FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        ).fetchone()

    if chamado is None:
        print(f"\nChamado com ID {id_chamado} não encontrado.")
        return

    print(f"\nChamado encontrado: {chamado['titulo']}")

    confirmacao = input(
        "Confirma a exclusão? Digite S para confirmar: "
    ).strip().upper()

    if confirmacao != "S":
        print("\nExclusão cancelada.")
        return

    with conectar_banco() as conexao:
        conexao.execute(
            """
            DELETE FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        )

    print(f"\nChamado {id_chamado} excluído com sucesso.")


def exibir_menu():
    while True:
        print("\n=== SISTEMA DE CHAMADOS DE TI ===")
        print("1 - Abrir chamado")
        print("2 - Listar chamados")
        print("3 - Buscar chamado por ID")
        print("4 - Atualizar status")
        print("5 - Excluir chamado")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_chamado()

        elif opcao == "2":
            listar_chamados()

        elif opcao == "3":
            buscar_chamado()

        elif opcao == "4":
            atualizar_status()

        elif opcao == "5":
            excluir_chamado()

        elif opcao == "0":
            print("\nSistema encerrado.")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    criar_tabela()
    exibir_menu()