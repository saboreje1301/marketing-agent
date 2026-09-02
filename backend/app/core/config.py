from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Marketing AI"

    DATABASE_URL: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "marketing_ai"
    DB_USER: str = "marketing_user"
    DB_PASSWORD: str = "marketing123"

    DEBUG: bool = True

    GOOGLE_ADS_DEVELOPER_TOKEN: str = ""
    GOOGLE_ADS_CLIENT_ID: str = ""
    GOOGLE_ADS_CLIENT_SECRET: str = ""
    GOOGLE_ADS_REFRESH_TOKEN: str = ""
    GOOGLE_ADS_CUSTOMER_ID: str = ""
    GOOGLE_ADS_LOGIN_CUSTOMER_ID: str = ""
    GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN: str = ""
    GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN: str = ""
    GOOGLE_SEARCH_CONSOLE_SITE_URL: str = ""
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.6-flash"
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
