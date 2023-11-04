from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI
from fastapi_router_controller import Controller

from hrflow.web.web_settings import WEB_SETTINGS


def create_app(controllers: Optional[List[Controller]] = None):
    app = FastAPI(
        debug=WEB_SETTINGS.debug,
        title=WEB_SETTINGS.title,
        version=WEB_SETTINGS.version,
    )

    if controllers:
        for controller in controllers:
            app.include_router(controller.router())
    return app
