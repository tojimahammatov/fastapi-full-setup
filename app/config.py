from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_user: str
    database_password: str

    algorithm: str
    secret_key: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
