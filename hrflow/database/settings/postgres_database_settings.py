from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from pydantic import validator
from sqlalchemy.engine.url import URL

from hrflow.database.settings.rdbms_settings import RDMBSSettings


class PostgresDatabaseSettings(RDMBSSettings):
    sql_alchemy_db_uri: Optional[str] = None

    @validator("sql_alchemy_db_uri")
    def assemble_db_connection_uri(cls, v: Optional[URL], values: Dict[str, Any]) -> str:
        return (
            URL.create(
                drivername="postgresql+asyncpg" if values.get("async_engine") else "postgresql",
                username=values.get("user"),
                password=values.get("password"),
                host=values.get("host"),
                port=values.get("port"),
                database=values.get("name")
            ).render_as_string(False)
        )
