
from hrflow.web.app_factory import create_app
from hrflow.web.global_di_container import GlobalDIContainer
from hrflow.web.apps.auth.app import auth_app
from hrflow.web.apps.jobpost.app import jobpost_app

def main_app():
    container = GlobalDIContainer()
    main_app = create_app()
    main_app.container = container
    @main_app.get("/health")
    def health_check():
        return "OK"
    main_app.mount("/auth", app=auth_app)
    main_app.mount("/job", app = jobpost_app)
    return main_app