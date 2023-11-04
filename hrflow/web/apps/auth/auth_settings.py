

from hrflow.common.base_settings import BaseEnvSettings


class AuthSettings(BaseEnvSettings):
    class Config:
        env_prefix = "auth_"
    secret_key:str = "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
    access_token_expire_minutes:int = 30*24*60
    algorithm: str = "HS256"