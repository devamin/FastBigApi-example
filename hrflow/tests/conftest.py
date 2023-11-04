from typing import Optional
import pytest
from hrflow.database.settings.sqlite_database_settings import SqliteDatabaseSettings
from hrflow.tests.web.apps.auth.test_auth_controller import TestAuthController
from hrflow.tests.web.apps.jobpost.test_jobpost_controller import TestJobPostController
from hrflow.web.app import main_app
from fastapi.testclient import TestClient

from hrflow.web.apps.jobpost.controller.jobpost_controller import JobPostController

@pytest.fixture(scope="session")
def client():
    sqlite_settings = SqliteDatabaseSettings()
    app= main_app()
    app.container.db_di_container.db_settings.override(sqlite_settings)
    app.container.db_di_container.sql_connection_manager() 
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == 'OK'
    yield client

@pytest.fixture(scope="session")
def mainuser_with_client(client):
    test_auth_controller = TestAuthController()
    user1 = test_auth_controller.test_signup(client=client, username="mainuser")
    return user1, client

@pytest.fixture
def user_with_client(client):
    def _user_with_client(username:Optional[str]="username", password:Optional[str]="password"):
        test_auth_controller = TestAuthController()
        user1 = test_auth_controller.test_signup(client=client,username=username, password=password)
        return user1, client
    return _user_with_client

@pytest.fixture(scope="session")
def get_main_jobpost(mainuser_with_client):
    test_jbpost_controller = TestJobPostController()
    jbpost = test_jbpost_controller.test_create_jobpost(mainuser_with_client=mainuser_with_client)
    return jbpost
   
   

    
