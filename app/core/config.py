from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import APP_TITLE, DATABASE_URL, DESCRIPTION


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    app_title: str = APP_TITLE
    description: str = DESCRIPTION
    database_url: Optional[str] = DATABASE_URL
    secret: str = 'SECRET'
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None


settings = Settings()
