
from dependency_injector import containers, providers
from hrflow.web.apps.auth.auth_di_container import AuthDIContainer
from hrflow.web.apps.auth.controller import auth_controller
from hrflow.web.apps.auth import auth_core
from hrflow.web.apps.jobpost.controller import jobpost_controller, application_controller
from hrflow.web.apps.jobpost.jobpost_di_container import JobPostDIContainer

from hrflow.web.db_di_container import DBDIContainer
from hrflow.web import core

class GlobalDIContainer(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(
        modules=[
            core,
            auth_controller,
            jobpost_controller,
            application_controller,
            auth_core
            ]
    )
     
    db_di_container = providers.Container(DBDIContainer)

    auth_di_container = providers.Container(AuthDIContainer)

    jobpost_di_container = providers.Container(JobPostDIContainer)