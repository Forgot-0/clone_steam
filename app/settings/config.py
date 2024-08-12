from pydantic import Field
from pydantic_settings import BaseSettings



class Email(BaseSettings):
    username: str = Field(alias="EMAIL_USERNAME")
    password: str = Field(alias="EMAIL_PASSWORD")
    from_email: str = Field(alias="EMAIL_FROM")
    port: int = Field(default=587, alias="EMAIL_PORT")
    server: str = Field(alias="EMAIL_SERVER")
    starttls: bool = Field(default=False, alias="EMAIL_STARTTLS")
    ssl_tls: bool = Field(default=True, alias="EMAIL_SSL_TLS")
    use_credentials: bool = Field(default=True, alias="USE_CREDENTIALS")
    validate_certs: bool = Field(default=True, alias="VALIDATE_CERTS")


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

