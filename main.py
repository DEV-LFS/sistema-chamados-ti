import sqlite3
from pathlib import Path


CAMINHO_BANCO = Path(__file__).resolve().parent / "chamados.db"


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    # Permite acessar as colunas pelo nome.
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
        print(f"\nID: {chamado['id']}")
        print(f"Título: {chamado['titulo']}")
        print(f"Descrição: {chamado['descricao']}")
        print(f"Categoria: {chamado['categoria']}")
        print(f"Prioridade: {chamado['prioridade']}")
        print(f"Status: {chamado['status']}")
        print(f"Data de criação: {chamado['data_criacao']}")
        print("-" * 40)


def exibir_menu():
    while True:
        print("\n=== SISTEMA DE CHAMADOS DE TI ===")
        print("1 - Abrir chamado")
        print("2 - Listar chamados")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_chamado()

        elif opcao == "2":
            listar_chamados()

        elif opcao == "0":
            print("\nSistema encerrado.")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


criar_tabela()
exibir_menu()