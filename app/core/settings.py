from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "stockOptions"
    VERSION: str = "0.0.1"

# Create a singleton instance
settings = Settings()