import os
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field


class PostgresConfig(BaseSettings):
    echo_log: bool = Field(default=False, env="DB_ECHO_LOG")
    host: str = Field(default="127.0.0.1", env="DB_HOST")
    port: str = Field(default="15432", env="DB_PORT")
    database: str = Field(default="line_provider_database", env="DB_NAME")
    user: str = Field(default="user", env="DB_USERNAME")
    password: str = Field(default="changeme", env="DB_PASSWORD")

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def migration_database_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class ProjectConfig(BaseSettings):
    name: str = Field("line-provider", env="PROJECT_NAME")
    api_host: str = Field(default="127.0.0.1", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=False, env="DEBUG")
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GRPServerConfig(BaseSettings):
    host: str = Field(default="0.0.0.0", env="GRPC_HOST")
    port: int = Field(default=50051, env="GRPC_PORT")
    auth_token: str = Field(default="", env="GRPC_AUTH_TOKEN")


class BetGRPCConfig(BaseSettings):
    host: str = Field(default="", env="BET_GRPC_HOST")
    port: int = Field(default=50051, env="BET_GRPC_PORT")
    postfix: Optional[str] = Field(default=None, env="BET_GRPC_POSTFIX")
    auth_token: str = Field(default="", env="BET_GRPC_TOKEN")

    @property
    def metadata(self):
        return [("authorization", f"Bearer {self.auth_token}")]

    @property
    def url(self):
        return f"{self.host}:{self.port}" + (f"/{self.postfix}" if self.postfix else "")


class Settings(BaseSettings):
    project: ProjectConfig = ProjectConfig()
    grpc_server: GRPServerConfig = GRPServerConfig()
    postgres: PostgresConfig = PostgresConfig()
    bet_grpc: BetGRPCConfig = BetGRPCConfig()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
