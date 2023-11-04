from typing import Any, Dict, Literal, Optional

from pydantic import validator

from hrflow.common.base_settings import ENV, AppTypeEnvironment
from hrflow.database.settings.database_settings import DatabaseSettings


class RDMBSSettings(DatabaseSettings):
    auto_create: bool = bool(ENV.environment in [AppTypeEnvironment.development, AppTypeEnvironment.test])
    sqlalchemy_pool_size: int = 50
    sqlalchemy_max_overflow: int = 100