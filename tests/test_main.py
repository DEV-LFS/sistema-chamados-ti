
import main


def test_terminal_impede_reabertura(
    tmp_path,
    monkeypatch,
    capsys
):
    banco_teste = tmp_path / "terminal_teste.db"

    monkeypatch.setattr(
        main,
        "CAMINHO_BANCO",
        banco_teste
    )

    main.criar_tabela()

    with main.conectar_banco() as conexao:
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
                "Computador sem internet",
                "Computador não acessa a rede.",
                "Rede",
                "Alta",
                "Fechado"
            )
        )

        id_chamado = cursor.lastrowid

    entradas = iter([str(id_chamado), "1"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entradas)
    )

    main.atualizar_status()

    saida = capsys.readouterr().out

    assert "transição de status não permitida" in saida

    with main.conectar_banco() as conexao:
        chamado = conexao.execute(
            """
            SELECT status
            FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        ).fetchone()

    assert chamado["status"] == "Fechado"


def test_terminal_permite_transicao_valida(
    tmp_path,
    monkeypatch,
    capsys
):
    banco_teste = tmp_path / "terminal_teste.db"

    monkeypatch.setattr(
        main,
        "CAMINHO_BANCO",
        banco_teste
    )

    main.criar_tabela()

    with main.conectar_banco() as conexao:
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
                "Monitor sem imagem",
                "O monitor não apresenta imagem.",
                "Hardware",
                "Alta",
                "Aberto"
            )
        )

        id_chamado = cursor.lastrowid

    entradas = iter([str(id_chamado), "2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entradas)
    )

    main.atualizar_status()

    saida = capsys.readouterr().out

    assert "atualizado para 'Em andamento'" in saida

    with main.conectar_banco() as conexao:
        chamado = conexao.execute(
            """
            SELECT status
            FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        ).fetchone()

    assert chamado is not None
    assert chamado["status"] == "Em andamento"


def test_terminal_impede_salto_de_status(
    tmp_path,
    monkeypatch,
    capsys
):
    banco_teste = tmp_path / "terminal_teste.db"

    monkeypatch.setattr(
        main,
        "CAMINHO_BANCO",
        banco_teste
    )

    main.criar_tabela()

    with main.conectar_banco() as conexao:
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
                "Computador com defeito",
                "O computador não está funcionando.",
                "Hardware",
                "Alta",
                "Aberto"
            )
        )

        id_chamado = cursor.lastrowid

    entradas = iter([str(id_chamado), "4"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entradas)
    )

    main.atualizar_status()

    saida = capsys.readouterr().out

    assert "transição de status não permitida" in saida

    with main.conectar_banco() as conexao:
        chamado = conexao.execute(
            """
            SELECT status
            FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        ).fetchone()

    assert chamado is not None
    assert chamado["status"] == "Aberto"
