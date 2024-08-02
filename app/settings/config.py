from pydantic import Field
from pydantic_settings import BaseSettings



class Email(BaseSettings):
    sender: str = Field(alias="EMAIL_SENDER")
    template_path: str = Field(alias='EMAIL_TEMPLATE_PATH')
    password: str = Field(alias='EMAIL_PASSWORD')


class API(BaseSettings):
    port: int = Field(alias='API_PORT')


class DataBase(BaseSettings):
    url: str = Field(alias='DATABASE_URL')
    username: str = Field(alias='DATABASE_USERNAME')
    password: str = Field(alias='DATABASE_PASSWORD')
    port: str = Field(alias='DATABASE_PORT')


class Config:
    db = DataBase()
    api = API()
    email = Email()

