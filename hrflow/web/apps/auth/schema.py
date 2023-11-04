


from pydantic import BaseModel, model_validator


class SignUpReq(BaseModel):
    username:str
    password:str
    password_confirmation:str

    @model_validator(mode='before')
    def validate(cls, values):
        if values['password'] != values['password_confirmation']:
            raise ValueError("Password confirmation doesn't match")
        return values


class UserWithTokenRes(BaseModel):
    id:int
    username:str
    access_token:str
    token_type: str = "Bearer"