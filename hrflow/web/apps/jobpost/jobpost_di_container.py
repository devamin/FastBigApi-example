from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from hrflow.web.apps.jobpost.privileges.jobpost_owner_privilege import JobPostOwnerPrivilege
from hrflow.web.apps.jobpost.repository.application_repository import ApplicationRepository

from hrflow.web.apps.jobpost.repository.jobpost_repository import JobPostRepository
from hrflow.web.apps.jobpost.service.application_service import ApplicationService
from hrflow.web.apps.jobpost.service.jobpost_service import JobPostService

class JobPostDIContainer(DeclarativeContainer):
    
    jobpost_repository = providers.Singleton(JobPostRepository)
    jobpost_service = providers.Singleton(JobPostService, jobpost_repository = jobpost_repository)

    application_repository = providers.Singleton(ApplicationRepository)
    application_service = providers.Singleton(
        ApplicationService,
        jobpost_service=jobpost_service,
        application_repository=application_repository)

    jobpost_owner_privilege = providers.Singleton(
        JobPostOwnerPrivilege, ressource_provider = jobpost_service.provided.get_jobpost_by_id
    )