import sqlite3
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


CAMINHO_BANCO = Path(__file__).resolve().parent / "chamados.db"


tags_metadata = [
    {
        "name": "Sistema",
        "description": "Verificação do funcionamento da API."
    },
    {
        "name": "Chamados",
        "description": "Operações de criação, consulta, atualização e exclusão."
    }
]


app = FastAPI(
    title="Sistema de Chamados de TI",
    description=(
        "API REST para gerenciamento de chamados técnicos, "
        "desenvolvida com Python, FastAPI e SQLite."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata
)


# ============================================================
# MODELOS DE ENTRADA
# ============================================================

class ChamadoCriacao(BaseModel):
    titulo: str = Field(
        min_length=3,
        max_length=100,
        examples=["Computador sem acesso à internet"]
    )

    descricao: str = Field(
        min_length=5,
        max_length=500,
        examples=["O computador não consegue acessar nenhum site."]
    )

    categoria: str = Field(
        min_length=3,
        max_length=50,
        examples=["Rede"]
    )

    prioridade: Literal[
        "Baixa",
        "Média",
        "Alta"
    ] = Field(
        examples=["Alta"]
    )


class ChamadoStatusAtualizacao(BaseModel):
    status: Literal[
        "Aberto",
        "Em andamento",
        "Resolvido",
        "Fechado"
    ] = Field(
        examples=["Em andamento"]
    )


# ============================================================
# MODELOS DE RESPOSTA
# ============================================================

class ChamadoResposta(BaseModel):
    id: int
    titulo: str
    descricao: str
    categoria: str
    prioridade: Literal[
        "Baixa",
        "Média",
        "Alta"
    ]
    status: Literal[
        "Aberto",
        "Em andamento",
        "Resolvido",
        "Fechado"
    ]
    data_criacao: str


class MensagemResposta(BaseModel):
    mensagem: str


class ChamadoExcluido(BaseModel):
    id: int
    titulo: str


class ExclusaoResposta(BaseModel):
    mensagem: str
    chamado_excluido: ChamadoExcluido


class ErroResposta(BaseModel):
    detail: str


# ============================================================
# BANCO DE DADOS
# ============================================================

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


# ============================================================
# ENDPOINT INICIAL
# ============================================================

@app.get(
    "/",
    response_model=MensagemResposta,
    tags=["Sistema"],
    summary="Verificar funcionamento da API",
    description="Retorna uma mensagem indicando que a API está funcionando."
)
def inicio():
    return {
        "mensagem": "API do Sistema de Chamados de TI está funcionando."
    }


# ============================================================
# LISTAR CHAMADOS
# ============================================================

@app.get(
    "/chamados",
    response_model=list[ChamadoResposta],
    tags=["Chamados"],
    summary="Listar todos os chamados",
    description="Retorna todos os chamados cadastrados no banco de dados."
)
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


# ============================================================
# BUSCAR CHAMADO POR ID
# ============================================================

@app.get(
    "/chamados/{id_chamado}",
    response_model=ChamadoResposta,
    tags=["Chamados"],
    summary="Buscar chamado por ID",
    description="Retorna um chamado específico a partir do seu ID.",
    responses={
        404: {
            "model": ErroResposta,
            "description": "Chamado não encontrado."
        }
    }
)
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


# ============================================================
# CRIAR CHAMADO
# ============================================================

@app.post(
    "/chamados",
    response_model=ChamadoResposta,
    status_code=201,
    tags=["Chamados"],
    summary="Criar novo chamado",
    description="Cria um novo chamado técnico no banco de dados."
)
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


# ============================================================
# ATUALIZAR STATUS
# ============================================================

@app.patch(
    "/chamados/{id_chamado}/status",
    response_model=ChamadoResposta,
    tags=["Chamados"],
    summary="Atualizar status do chamado",
    description=(
        "Atualiza o status de um chamado para Aberto, "
        "Em andamento, Resolvido ou Fechado."
    ),
    responses={
        404: {
            "model": ErroResposta,
            "description": "Chamado não encontrado."
        }
    }
)
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


# ============================================================
# EXCLUIR CHAMADO
# ============================================================

@app.delete(
    "/chamados/{id_chamado}",
    response_model=ExclusaoResposta,
    tags=["Chamados"],
    summary="Excluir chamado",
    description="Exclui definitivamente um chamado do banco de dados.",
    responses={
        404: {
            "model": ErroResposta,
            "description": "Chamado não encontrado."
        }
    }
)
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