from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DB(BaseModel):
    url: PostgresDsn = 'postgresql+psycopg2://postgres:postgres@db:5432/db'


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_nested_delimiter='__'
    )

    token: str
    DB: DB


config = Config().model_dump()
