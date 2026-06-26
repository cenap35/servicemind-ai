from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ServiceMind AI API"
    app_description: str = "AI-powered automotive intelligence platform."
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"


settings = Settings()