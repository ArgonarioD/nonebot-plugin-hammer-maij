from pydantic import BaseModel, validator


class Config(BaseModel):
    maij_api_token: str
    maij_api_root_url: str = 'https://api.argonariod.tech/maij'

    @validator("maij_api_token")
    def check_token(cls, v):
        if isinstance(v, str):
            return v
        raise ValueError("maij_api_token must be str")
