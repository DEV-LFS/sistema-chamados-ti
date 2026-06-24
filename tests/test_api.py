import pytest
from fastapi.testclient import TestClient

import api


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    """
    Cria um banco SQLite temporário para cada teste.

    Isso impede que os testes alterem o banco real do projeto.
    """
    banco_teste = tmp_path / "chamados_teste.db"

    monkeypatch.setattr(
        api,
        "CAMINHO_BANCO",
        banco_teste
    )

    api.criar_tabela()

    with TestClient(api.app) as cliente_teste:
        yield cliente_teste


def criar_chamado_teste(cliente):
    resposta = cliente.post(
        "/chamados",
        json={
            "titulo": "Computador sem internet",
            "descricao": "O computador não consegue acessar nenhum site.",
            "categoria": "Rede",
            "prioridade": "Alta"
        }
    )

    assert resposta.status_code == 201

    return resposta.json()


def test_verificar_funcionamento_api(cliente):
    resposta = cliente.get("/")

    assert resposta.status_code == 200

    assert resposta.json() == {
        "mensagem": (
            "API do Sistema de Chamados de TI está funcionando."
        )
    }


def test_criar_chamado(cliente):
    resposta = cliente.post(
        "/chamados",
        json={
            "titulo": "Monitor sem imagem",
            "descricao": "O monitor liga, mas não apresenta imagem.",
            "categoria": "Hardware",
            "prioridade": "Alta"
        }
    )

    dados = resposta.json()

    assert resposta.status_code == 201
    assert dados["id"] == 1
    assert dados["titulo"] == "Monitor sem imagem"
    assert dados["categoria"] == "Hardware"
    assert dados["prioridade"] == "Alta"
    assert dados["status"] == "Aberto"
    assert "data_criacao" in dados


def test_listar_chamados(cliente):
    chamado = criar_chamado_teste(cliente)

    resposta = cliente.get("/chamados")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert len(dados) == 1
    assert dados[0]["id"] == chamado["id"]
    assert dados[0]["titulo"] == chamado["titulo"]


def test_buscar_chamado_por_id(cliente):
    chamado = criar_chamado_teste(cliente)

    resposta = cliente.get(
        f"/chamados/{chamado['id']}"
    )

    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados["id"] == chamado["id"]
    assert dados["titulo"] == chamado["titulo"]


def test_buscar_chamado_inexistente(cliente):
    resposta = cliente.get("/chamados/999")

    assert resposta.status_code == 404

    assert resposta.json() == {
        "detail": "Chamado com ID 999 não encontrado."
    }


def test_atualizar_status_chamado(cliente):
    chamado = criar_chamado_teste(cliente)

    resposta = cliente.patch(
        f"/chamados/{chamado['id']}/status",
        json={
            "status": "Em andamento"
        }
    )

    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados["id"] == chamado["id"]
    assert dados["status"] == "Em andamento"


def test_rejeitar_status_invalido(cliente):
    chamado = criar_chamado_teste(cliente)

    resposta = cliente.patch(
        f"/chamados/{chamado['id']}/status",
        json={
            "status": "Cancelado"
        }
    )

    assert resposta.status_code == 422


def test_excluir_chamado(cliente):
    chamado = criar_chamado_teste(cliente)

    resposta_exclusao = cliente.delete(
        f"/chamados/{chamado['id']}"
    )

    assert resposta_exclusao.status_code == 200

    dados_exclusao = resposta_exclusao.json()

    assert dados_exclusao["chamado_excluido"]["id"] == chamado["id"]

    resposta_busca = cliente.get(
        f"/chamados/{chamado['id']}"
    )

    assert resposta_busca.status_code == 404