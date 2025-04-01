from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_token: str = Field(
        "",
        alias="API_TOKEN",
        env="API_TOKEN",
    )
    
    gigachat_auth_key: str = Field(
        "",
        alias="GIGACHAT_AUTH_KEY",
        env="GIGACHAT_AUTH_KEY",
    )
    
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    

settings = Settings()
    