from pwdlib import PasswordHash

"""Operações de hash e verificação de senhas."""
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Gera o hash seguro de uma senha."""
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica uma senha contra seu hash armazenado."""
    return password_hash.verify(password, hashed_password)