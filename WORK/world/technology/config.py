from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    AUTH_TOKEN: str
    ACCESS_TOKEN: str   

settings = Settings()

print(settings.model_config['env_file'])