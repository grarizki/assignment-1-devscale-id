from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "stockOptions"
    VERSION: str = "0.0.1"
    database_url: str = "sqlite:///./database.db"


# Create a singleton instance
settings = Settings()
