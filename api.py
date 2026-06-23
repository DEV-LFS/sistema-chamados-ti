import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException


CAMINHO_BANCO = Path(__file__).resolve().parent / "chamados.db"


app = FastAPI(
    title="Sistema de Chamados de TI",
    description="API REST para gerenciamento de chamados técnicos.",
    version="1.0.0"
)


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
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