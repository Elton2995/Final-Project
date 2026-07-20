from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class LoggingConfig(BaseSettings):
    """Logging configuration."""
    
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/app.log", env="LOG_FILE")
    LOG_MAX_BYTES: int = Field(default=10485760, env="LOG_MAX_BYTES")  # 10MB
    LOG_BACKUP_COUNT: int = Field(default=5, env="LOG_BACKUP_COUNT")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s",
        env="LOG_FORMAT"
    )
    LOG_DATE_FORMAT: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        env="LOG_DATE_FORMAT"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"