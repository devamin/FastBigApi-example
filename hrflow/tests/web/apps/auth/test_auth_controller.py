

from typing import Optional
from fastapi.testclient import TestClient

from hrflow.web.apps.auth.schema import UserWithTokenRes


class TestAuthController:

    def test_signup(self,client:TestClient, username:Optional[str]="username1", password:Optional[str]="password1")->UserWithTokenRes:
        
        res = client.post("/auth/signup", json={
            "username":username,
            "password":password,
            "password_confirmation":password
        })
        assert res.status_code == 200
        #Validate the response schema
        return UserWithTokenRes(**res.json())


    def test_login(self, client:TestClient)->UserWithTokenRes:
        res = client.post("/auth/login", data={
            "username":"username1",
            "password":"password1"
        })
        assert res.status_code == 200
        #Validate the response schema
        return UserWithTokenRes(**res.json())

    def test_signup_same_user(self,client:TestClient):
        res = client.post("/auth/signup", json={
            "username":"username1",
            "password":"password1",
            "password_confirmation":"password1"
        })
        assert res.status_code == 403

    def test_signup_wrong_input(self,client:TestClient):
        res = client.post("/auth/signup", json={
            "username":"username1",
            "password":"22222",
            "password_confirmation":"password1"
        })
        assert res.status_code == 422

    def test_login_wrong_credentials(self, client:TestClient):
        res = client.post("/auth/login", data={
            "username":"username1",
            "password":"password2221"
        })
        assert res.status_code == 403
