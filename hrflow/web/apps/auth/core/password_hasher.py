from __future__ import annotations

from passlib.context import CryptContext


class PasswordHasher:
    def __init__(self, crypt_context: CryptContext):
        self.crypt_context = crypt_context

    def hash_password(self, password: str):
        return self.crypt_context.hash(password)

    def verfiy_password(self, plain_password: str, hashed_password):
        return self.crypt_context.verify(plain_password, hashed_password)
