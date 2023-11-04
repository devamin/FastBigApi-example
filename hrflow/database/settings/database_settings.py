from __future__ import annotations

from typing import Any, Dict, Optional

from hrflow.common.base_settings import ENV, BaseEnvSettings
from hrflow.database.constants import DBSoftware
from pydantic import field_validator


class DatabaseSettings(BaseEnvSettings):
    class Config:
        env_prefix = "db_"

    user: str = "postgres"
    password: str = "postgres"
    port: int = 5423
    host: str = "127.0.0.1"
    async_engine: bool = False
    name: Optional[str] = None
    software: DBSoftware = DBSoftware.sqlite
    # Let this to be controlled with the logger instead of settings
    # bool(ENV.environment in [AppTypeEnvironment.development, AppTypeEnvironment.test])
    echo: bool = False

    @field_validator("name", mode="before")
    @classmethod
    def default_db_name(cls, v: Optional[str]) -> str:
        if isinstance(v, str):
            return v
        return f"hrflow_{ENV}"
