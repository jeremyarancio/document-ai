from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


REPO_DIR = Path(__file__).parent.parent.parent


class StorageSettings(BaseModel):
    dir: Path = REPO_DIR / "data/storage"


class DocumentSourceSettings(BaseModel):
    query: str = "Deepseek"
    limit: int = 10


class DBSettings(BaseModel):
    path: Path = REPO_DIR / "data/duck.db"
    document_table_name: str = "documents"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    storage: StorageSettings = StorageSettings()
    source: DocumentSourceSettings = DocumentSourceSettings()
    db: DBSettings = DBSettings()


def get_settings() -> Settings:
    return Settings()
