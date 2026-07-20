import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import settings

def setup_logging():
    """Setup application logging configuration."""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    log_file = settings.LOG_FILE
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    root_logger.addHandler(file_handler)
    
    # Log startup message
    root_logger.info("=" * 60)
    root_logger.info(f"ServiceDesk Backend v{settings.APP_VERSION}")
    root_logger.info(f"Environment: {settings.ENVIRONMENT}")
    root_logger.info(f"Log Level: {settings.LOG_LEVEL}")
    root_logger.info("=" * 60)
    
    return root_logger

# Global logger instance
logger = logging.getLogger('app')