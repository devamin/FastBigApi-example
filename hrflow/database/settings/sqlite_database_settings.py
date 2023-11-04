import tempfile
from typing import Any, Dict, Optional

from pydantic import root_validator, validator
from sqlalchemy.engine.url import URL
from hrflow.database.constants import DBSoftware

from hrflow.database.settings.database_settings import DatabaseSettings


class SqliteDatabaseSettings(DatabaseSettings):
    sql_alchemy_db_uri: Optional[str] = None
    sqlite_filepath:Optional[str] = None
    software: DBSoftware = DBSoftware.sqlite
    @validator("sql_alchemy_db_uri", pre=False)
    def assemble_db_connection_uri(cls, v: Optional[URL], values: Dict[str, Any]) -> str:
        driver = "sqlite+aiosqlite" if values.get("async_engine") else "sqlite"
        destination = values.get("sqlite_filepath") if values.get("sqlite_filepath") else ":memory:"
        return f"{driver}:///{destination}"

