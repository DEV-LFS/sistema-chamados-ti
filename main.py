import json
from pathlib import Path


ARQUIVO_CHAMADOS = Path("chamados.json")


def carregar_chamados():
    if not ARQUIVO_CHAMADOS.exists():
        return []

    try:
        with open(ARQUIVO_CHAMADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError:
        print("Aviso: o arquivo de chamados está corrompido.")
        return []


def salvar_chamados():
    with open(ARQUIVO_CHAMADOS, "w", encoding="utf-8") as arquivo:
        json.dump(
            chamados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


chamados = carregar_chamados()


def criar_chamado():
    print("\n--- ABRIR NOVO CHAMADO ---")

    titulo = input("Título do problema: ")
    descricao = input("Descrição do problema: ")
    categoria = input("Categoria: ")
    prioridade = input("Prioridade (Baixa, Média ou Alta): ")

    chamado = {
        "id": len(chamados) + 1,
        "titulo": titulo,
        "descricao": descricao,
        "categoria": categoria,
        "prioridade": prioridade,
        "status": "Aberto"
    }

    chamados.append(chamado)
    salvar_chamados()

    print("\nChamado criado e salvo com sucesso!")


def listar_chamados():
    print("\n--- LISTA DE CHAMADOS ---")

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
        print("-" * 30)


def exibir_menu():
    while True:
        print("\n=== SISTEMA DE CHAMADOS DE TI ===")
        print("1 - Abrir chamado")
        print("2 - Listar chamados")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_chamado()

        elif opcao == "2":
            listar_chamados()

        elif opcao == "0":
            print("\nSistema encerrado.")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


exibir_menu()