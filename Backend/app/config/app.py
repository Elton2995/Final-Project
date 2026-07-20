from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class AppConfig(BaseSettings):
    """Application configuration."""
    
    APP_NAME: str = Field(default="ServiceDesk", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    API_PREFIX: str = Field(default="/api/v1", env="API_PREFIX")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        env="CORS_ORIGINS"
    )
    
    # Uploads
    UPLOAD_DIR: str = Field(default="uploads", env="UPLOAD_DIR")
    MAX_UPLOAD_SIZE: int = Field(default=5242880, env="MAX_UPLOAD_SIZE")  # 5MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"