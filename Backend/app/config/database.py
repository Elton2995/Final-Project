from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class DatabaseConfig(BaseSettings):
    """Database configuration."""
    
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")
    DATABASE_ECHO: bool = Field(default=False, env="DATABASE_ECHO")
    DATABASE_POOL_PRE_PING: bool = Field(default=True, env="DATABASE_POOL_PRE_PING")
    DATABASE_POOL_RECYCLE: int = Field(default=3600, env="DATABASE_POOL_RECYCLE")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"