from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class EnvSettings(BaseSettings):
    OPENAI_API_KEY: str = None
    MONGODB_ATLAS_URI: str = None
    MONGODB_DATABASE: str = "IllnessQA"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
