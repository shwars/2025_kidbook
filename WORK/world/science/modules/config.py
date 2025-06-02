from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gigachat_auth_key: str = Field(
        "",
        alias="GIGACHAT_AUTH_KEY",
        env="GIGACHAT_AUTH_KEY",
    )
    
    kidbook_path: str = Field(
        "",
        alias="KIDBOOK_PATH",
        env="KIDBOOK_PATH",
    )
    
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    

settings = Settings()
    