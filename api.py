import sqlite3
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


CAMINHO_BANCO = Path(__file__).resolve().parent / "chamados.db"


app = FastAPI(
    title="Sistema de Chamados de TI",
    description="API REST para gerenciamento de chamados técnicos.",
    version="1.0.0"
)


class ChamadoCriacao(BaseModel):
    titulo: str = Field(
        min_length=3,
        max_length=100
    )

    descricao: str = Field(
        min_length=5,
        max_length=500
    )

    categoria: str = Field(
        min_length=3,
        max_length=50
    )

    prioridade: Literal[
        "Baixa",
        "Média",
        "Alta"
    ]


class ChamadoStatusAtualizacao(BaseModel):
    status: Literal[
        "Aberto",
        "Em andamento",
        "Resolvido",
        "Fechado"
    ]


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


criar_tabela()


@app.get("/")
def inicio():
    return {
        "mensagem": "API do Sistema de Chamados de TI está funcionando."
    }


@app.get("/chamados")
def listar_chamados():
    with conectar_banco() as conexao:
        registros = conexao.execute(
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

    return [dict(registro) for registro in registros]


@app.get("/chamados/{id_chamado}")
def buscar_chamado(id_chamado: int):
    if id_chamado <= 0:
        raise HTTPException(
            status_code=422,
            detail="O ID precisa ser maior que zero."
        )

    with conectar_banco() as conexao:
        registro = conexao.execute(
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

    if registro is None:
        raise HTTPException(
            status_code=404,
            detail=f"Chamado com ID {id_chamado} não encontrado."
        )

    return dict(registro)


@app.post("/chamados", status_code=201)
def criar_chamado(dados: ChamadoCriacao):
    titulo = dados.titulo.strip()
    descricao = dados.descricao.strip()
    categoria = dados.categoria.strip()

    if not titulo or not descricao or not categoria:
        raise HTTPException(
            status_code=422,
            detail="Os campos não podem conter apenas espaços."
        )

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
                dados.prioridade,
                "Aberto"
            )
        )

        id_chamado = cursor.lastrowid

        registro = conexao.execute(
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

    return dict(registro)


@app.patch("/chamados/{id_chamado}/status")
def atualizar_status_chamado(
    id_chamado: int,
    dados: ChamadoStatusAtualizacao
):
    if id_chamado <= 0:
        raise HTTPException(
            status_code=422,
            detail="O ID precisa ser maior que zero."
        )

    with conectar_banco() as conexao:
        chamado_existente = conexao.execute(
            """
            SELECT id
            FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        ).fetchone()

        if chamado_existente is None:
            raise HTTPException(
                status_code=404,
                detail=f"Chamado com ID {id_chamado} não encontrado."
            )

        conexao.execute(
            """
            UPDATE chamados
            SET status = ?
            WHERE id = ?
            """,
            (
                dados.status,
                id_chamado
            )
        )

        chamado_atualizado = conexao.execute(
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

    return dict(chamado_atualizado)

@app.delete("/chamados/{id_chamado}")
def excluir_chamado(id_chamado: int):
    if id_chamado <= 0:
        raise HTTPException(
            status_code=422,
            detail="O ID precisa ser maior que zero."
        )

    with conectar_banco() as conexao:
        chamado_existente = conexao.execute(
            """
            SELECT id, titulo
            FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        ).fetchone()

        if chamado_existente is None:
            raise HTTPException(
                status_code=404,
                detail=f"Chamado com ID {id_chamado} não encontrado."
            )

        conexao.execute(
            """
            DELETE FROM chamados
            WHERE id = ?
            """,
            (id_chamado,)
        )

    return {
        "mensagem": f"Chamado {id_chamado} excluído com sucesso.",
        "chamado_excluido": {
            "id": chamado_existente["id"],
            "titulo": chamado_existente["titulo"]
        }
    }