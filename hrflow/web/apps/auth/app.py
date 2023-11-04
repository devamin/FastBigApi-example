from hrflow.web.app_factory import create_app
from hrflow.web.apps.auth.controller import controllers

auth_app = create_app(controllers = controllers)