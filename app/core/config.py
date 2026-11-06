from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DeepGuard Backend"
    # Local-only defaults. Docker Compose overrides these through environment variables.
    database_url: str = "postgresql+psycopg://deepguard:deepguard@localhost:5432/deepguard"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
