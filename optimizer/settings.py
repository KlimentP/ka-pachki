from pydantic import BaseSettings


class Settings(BaseSettings):
    USERNAME: str
    PASSWORD: str
    PROD: bool
    class Config:
        env_file = ".env"

settings = Settings() 