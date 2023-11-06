from __future__ import annotations

import asyncio
import logging
from typing import Optional, Union

from sqlalchemy import MetaData, QueuePool, StaticPool
from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy import text
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.elements import TextClause
from sqlalchemy_utils import create_database, database_exists

from hrflow.database import models
from hrflow.database.connection.transaction_base import TransactionBase
from hrflow.database.settings import DatabaseSettings, SqliteDatabaseSettings
from hrflow.database.settings.postgres_database_settings import PostgresDatabaseSettings

logger = logging.getLogger(__name__)


class SQLConnectionManager(TransactionBase):
    def __init__(
        self,
        db_settings: DatabaseSettings,
        create_schema: bool = True,
        engine: Optional[Union[Engine, AsyncEngine]] = None,
    ):
        self.db_settings = db_settings
        self.create_schema: bool = create_schema
        self.engine = engine if engine else self.create_engine()
        self._session_cls = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        base = models.get_declarative_base()
        self._metadata: MetaData = base.metadata
        self._metadata.create_all(self.engine)  
        print("created")

    @property
    def ping_statement(self) -> str:
        ping_stmt: TextClause = text("SELECT 1")
        return ping_stmt

    def execute_single_query(self, stmt: Union[str, TextClause]) -> Result:
        if isinstance(stmt, str):
            stmt = text(stmt)
        sql_session: Session
        with self.begin() as sql_session:
            result: Result = sql_session.execute(stmt)

        return result

    def create_engine(self):

        if isinstance(self.db_settings, SqliteDatabaseSettings):
            if self.db_settings.async_engine:
                engine = create_async_engine(
                    self.db_settings.sql_alchemy_db_uri,
                    connect_args={"check_same_thread": False},
                    echo=self.db_settings.echo,
                    poolclass=StaticPool if 'memory' in self.db_settings.sql_alchemy_db_uri else QueuePool
                )
            else:
                engine = create_sync_engine(
                    self.db_settings.sql_alchemy_db_uri,
                    connect_args={"check_same_thread": False},
                    echo=self.db_settings.echo,
                    poolclass=StaticPool if 'memory' in self.db_settings.sql_alchemy_db_uri else QueuePool
                )

        elif isinstance(
            self.db_settings, PostgresDatabaseSettings
        ):
            if self.db_settings.auto_create and not database_exists(self.db_settings.sql_alchemy_db_uri):
                logger.info(f"Create database under the name of {self.db_settings.name}")
                create_database(self.db_settings.sql_alchemy_db_uri)
                logger.info("DB Successufully Created")

            if self.db_settings.async_engine:
                engine = create_async_engine(
                    self.db_settings.sql_alchemy_db_uri,
                    pool_pre_ping=True,
                    pool_size=self.db_settings.sqlalchemy_pool_size,
                    max_overflow=self.db_settings.sqlalchemy_max_overflow,
                    echo=self.db_settings.echo,
                )
            else:
                engine = create_sync_engine(
                    self.db_settings.sql_alchemy_db_uri,
                    pool_pre_ping=True,
                    pool_size=self.db_settings.sqlalchemy_pool_size,
                    max_overflow=self.db_settings.sqlalchemy_max_overflow,
                    echo=self.db_settings.echo,
                )

        return engine

    def get_new_session(self):
        session: Session = self._session_cls()
        session.connection().execute(self.ping_statement)
        return session

    def close(self):
        if self.db_settings.async_engine:
            if self.engine:
                asyncio.create_task(self.engine.dispose())
