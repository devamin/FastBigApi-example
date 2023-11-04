from __future__ import annotations

from hrflow.common.str_enum import StrEnum


class DBSoftware(StrEnum):
    mysql = "mysql"
    sqlite = "sqlite"
    postgres = "postgres"


AUTH_CODE_LENGHT = 6
