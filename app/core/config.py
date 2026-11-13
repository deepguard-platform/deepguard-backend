from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DeepGuard Backend"
    # Local defaults. Docker Compose overrides these through environment variables.
    database_url: str = "sqlite:///./demo.db"
    redis_url: str = "redis://localhost:6379/0"
    model_url_mode: str = "local"
    max_upload_mb: int = 50

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
