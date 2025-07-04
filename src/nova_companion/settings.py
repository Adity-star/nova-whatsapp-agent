import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.logger import logging


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    GROQ_API_KEY: str
    TOGETHER_API_KEY: str
    ELEVENLABS_VOICE_ID: str
    ELEVENLABS_API_KEY: str

    QDRANT_API_KEY: str | None
    QDRANT_URL: str
    QDRANT_PORT: str = "6333"
    QDRANT_HOST: str | None = None

    TEXT_MODEL_NAME: str = "llama-3.3-70b-versatile"
    SMALL_TEXT_MODEL_NAME: str = "gemma2-9b-it"
    STT_MODEL_NAME: str = "whisper-large-v3-turbo"
    TTS_MODEL_NAME: str = "eleven_flash_v2_5"
    TTI_MODEL_NAME: str = "black-forest-labs/FLUX.1-schnell-Free"
    ITT_MODEL_NAME: str = "llama-3.2-90b-vision-preview"

    ROUTER_MESSAGES_TO_ANALYZE: int = 3
    MEMORY_TOP_K: int = 3
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 20
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5

    SHORT_TERM_MEMORY_DB_PATH: str = "data/memory.db"

    def __init__(self, *args, **kwargs):
        logging.info("Instantiating Settings")
        super().__init__(*args, **kwargs)
        # Ensure the directory for the database exists
        os.makedirs(os.path.dirname(self.SHORT_TERM_MEMORY_DB_PATH), exist_ok=True)


settings = Settings()
logging.info("Settings instance created")
