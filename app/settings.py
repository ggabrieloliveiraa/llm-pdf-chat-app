from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

class Settings(BaseSettings):
    # --- Google Gemini (principal) ---
    google_api_key: str = Field(..., alias="GOOGLE_API_KEY")

    # --- OpenAI (opcional / legado) ---
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    # RAG tuneables
    chunk_size: int = 1000
    chunk_overlap: int = 150

    # default chat model (Gemini‑Pro)
    model_name: str = "gemini-1.5-flash"

    model_config = ConfigDict(extra="ignore", case_sensitive=False)

settings = Settings(_env_file=".env")