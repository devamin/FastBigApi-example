from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings

from hrflow.common.str_enum import StrEnum


class AppTypeEnvironment(StrEnum):
    production: str = "production"
    development: str = "development"
    staging: str = "staging"
    test: str = "test"

    @classmethod
    def default(cls):
        return cls.development


class Environment(BaseSettings):
    environment: AppTypeEnvironment = Field(default_factory=AppTypeEnvironment.default)

    def __str__(self):
        return self.environment.value

    def __eq__(self, other):
        if isinstance(other, AppTypeEnvironment):
            return self.environment == other
        elif isinstance(other, Environment):
            return self.environment == other.environment
        elif isinstance(other, str):
            return str(self.environment) == other
        return False


ENV = Environment()


class BaseEnvSettings(BaseSettings):
    class Config:
        file_suffix = f".{ENV}"
        env_file = f".env{file_suffix}"
        env_prefix = "app_"

    env: Environment = ENV
    debug: bool = bool(ENV.environment in [AppTypeEnvironment.development, AppTypeEnvironment.staging])
    project_name: str = "Swippro"
    log_level: str = "INFO"


base_settings = BaseEnvSettings()
