async def refresh_tokens(token: str) -> RefreshResponse:
"""Valida o token recebido, consulta o hash, revoga o token atual e emite novos tokens"""

