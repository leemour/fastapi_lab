from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Reads from real env; in dev also reads from .env
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "Fastapi Lab"
    environment: str = Field(default="dev", description="dev|staging|prod")

    # n8n/service-to-service auth
    api_key: str = Field(default="change-me")

    # later:
    # database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/app"
    # storage_bucket: str = "..."
    # s3_endpoint: str = "..."


settings = Settings()
