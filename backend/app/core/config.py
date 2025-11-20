from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    MAX_TOKENS: int = Field(2000, env="MAX_TOKENS")
    TEMPERATURE: float = Field(0.2, env="TEMPERATURE")
    SUPABASE_DB_URL: str = Field(..., env="SUPABASE_DB_URL")

settings = Settings()
