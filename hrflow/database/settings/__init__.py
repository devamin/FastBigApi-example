from __future__ import annotations
from hrflow.database.constants import DBSoftware

from hrflow.database.settings.database_settings import DatabaseSettings
from hrflow.database.settings.postgres_database_settings import PostgresDatabaseSettings
from hrflow.database.settings.sqlite_database_settings import SqliteDatabaseSettings

__all__ = ["DatabaseSettings", "MysqlDatabaseSettings", "SqliteDatabaseSettings"]


def get_default_db_settings():
    settings = DatabaseSettings()
    if settings.software == DBSoftware.postgres:
        return PostgresDatabaseSettings()
    elif settings.software == DBSoftware.sqlite:
        return SqliteDatabaseSettings()
    raise Exception("We no longer support these databases, please use postgres")