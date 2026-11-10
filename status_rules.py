
# ============================================================
# REGRAS DE TRANSICAO DE STATUS
# ============================================================

TRANSICOES_PERMITIDAS = {
    "Aberto": {"Em andamento"},
    "Em andamento": {"Resolvido"},
    "Resolvido": {"Fechado"},
    "Fechado": set()
}


def transicao_permitida(
    status_atual: str,
    novo_status: str
) -> bool:
    if status_atual == novo_status:
        return True

    proximos_status = TRANSICOES_PERMITIDAS.get(
        status_atual,
        set()
    )

    return novo_status in proximos_status
