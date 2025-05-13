import hashlib
import time
import jwt


class Helper:
    @classmethod
    def generate_hash_password(cls, password: str) -> str:
        salt = "secret_salt_key"
        return (
            hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ":" + salt
        )

    @classmethod
    def match_hash_text(cls, hashed_text: str, provided_text: str) -> bool:
        _hashedText, salt = hashed_text.split(":")
        return (
            _hashedText
            == hashlib.sha256(salt.encode() + provided_text.encode()).hexdigest()
        )

    @classmethod
    def generate_access_token(cls, payload: dict) -> str:
        return jwt.encode(
            {"payload": payload, "exp": int(time.time()) + 10000},
            "secret_key",
            algorithm="HS256",
        )

    @classmethod
    def generate_refresh_token(cls, payload: dict) -> str:
        return jwt.encode({"payload": payload}, "secret_key", algorithm="HS256")

    @classmethod
    def decode_jwt(cls, token: str):
        decoded_token = jwt.decode(token, "secret_key", algorithms=["HS256"])
        id = decoded_token["payload"]["user_id"]
        return id
