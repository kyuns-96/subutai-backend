from typing import ClassVar

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "mysql+asyncmy://root:rootpassword@localhost:3306/subutai?charset=utf8mb4"
    )
    jwt_secret: str  # Required — set SUBUTAI_JWT_SECRET env var
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="SUBUTAI_"
    )


settings = Settings()  # pyright: ignore[reportCallIssue]
