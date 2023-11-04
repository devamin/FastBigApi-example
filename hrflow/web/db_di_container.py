from __future__ import annotations

from dependency_injector import containers, providers
from hrflow.database.connection.sql_connection_manager import SQLConnectionManager

from hrflow.database.settings import get_default_db_settings


class DBDIContainer(containers.DeclarativeContainer):

    db_settings = providers.Callable(get_default_db_settings)

    sql_connection_manager = providers.Singleton(SQLConnectionManager, db_settings=db_settings)

    session = providers.ContextLocalSingleton(sql_connection_manager.provided.begin)
