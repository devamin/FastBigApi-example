from hrflow.web.app_factory import create_app
from hrflow.web.apps.jobpost.controller import controllers

jobpost_app = create_app(controllers = controllers)