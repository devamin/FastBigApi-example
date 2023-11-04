from __future__ import annotations

from typing import List

from hrflow.common.base_settings import BaseEnvSettings


class WebSettings(BaseEnvSettings):
    class Config:
        env_prefix = "web_"

    version: str = "0.1.0"
    title: str = "HRFlow API"
    #allow_origins = ["https://hrflow.com/", "https://www.hrflow.com/"]
    allow_origins:List[str] = []
    port: int = 8989
    host: str = "127.0.0.1"


WEB_SETTINGS = WebSettings()