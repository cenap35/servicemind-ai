from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ServiceMind AI API"
    app_description: str = "AI-powered automotive intelligence platform."
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    ollama_url: str = "http://127.0.0.1:11434/api/generate"
    ollama_model: str = "qwen2.5:3b"


settings = Settings()