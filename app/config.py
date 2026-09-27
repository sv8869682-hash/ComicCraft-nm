from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_text_model: str = "gemini-2.5-flash"
    gemini_image_model: str = "gemini-3.1-flash-image"
    image_provider: str = "gemini"  # gemini | huggingface | placeholder
    hf_token: str = ""
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    app_name: str = "ComicCraft"
    debug: bool = True
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"
for folder in (PANELS_DIR, EXPORTS_DIR):
    folder.mkdir(parents=True, exist_ok=True)
