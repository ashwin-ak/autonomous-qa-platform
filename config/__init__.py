"""Configuration management for Autonomous QA Platform."""

import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class OpenAIConfig(BaseSettings):
    """OpenAI configuration."""

    api_key: str = Field(default="", env="OPENAI_API_KEY")
    model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    temperature: float = Field(default=0.1, env="OPENAI_TEMPERATURE")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    timeout: int = Field(default=60, env="OPENAI_TIMEOUT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class PlaywrightConfig(BaseSettings):
    """Playwright configuration."""

    timeout: int = Field(default=30000, env="PLAYWRIGHT_TIMEOUT")
    headless: bool = Field(default=True, env="PLAYWRIGHT_HEADLESS")
    browser: str = Field(default="chromium", env="PLAYWRIGHT_BROWSER")
    slow_down: int = Field(default=0, env="PLAYWRIGHT_SLOW_DOWN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class LoggingConfig(BaseSettings):
    """Logging configuration."""

    level: str = Field(default="INFO", env="LOG_LEVEL")
    file: str = Field(default="logs/autonomous-qa.log", env="LOG_FILE")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class DatabaseConfig(BaseSettings):
    """Database configuration."""

    chromadb_path: str = Field(default="./data/chromadb", env="CHROMADB_PATH")
    persist_dir: str = Field(default="./data/persist", env="PERSIST_DIRECTORY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class TestExecutionConfig(BaseSettings):
    """Test execution configuration."""

    grid_size: int = Field(default=4, env="TEST_GRID_SIZE")
    max_duration: int = Field(default=3600, env="TEST_MAX_DURATION")
    test_type: str = Field(default="full", env="TEST_TYPE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class APIConfig(BaseSettings):
    """API configuration."""

    host: str = Field(default="0.0.0.0", env="API_HOST")
    port: int = Field(default=8000, env="API_PORT")
    reload: bool = Field(default=True, env="API_RELOAD")
    log_level: str = Field(default="info", env="API_LOG_LEVEL")
    cors_enabled: bool = Field(default=True, env="API_CORS_ENABLED")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class Config(BaseSettings):
    """Main configuration class."""

    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    playwright: PlaywrightConfig = Field(default_factory=PlaywrightConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    test_execution: TestExecutionConfig = Field(default_factory=TestExecutionConfig)
    api: APIConfig = Field(default_factory=APIConfig)

    def __init__(self, **data):
        super().__init__(**data)
        self._validate_required_fields()
        self._validate_paths()
        self._setup_logging()

    def _validate_required_fields(self) -> None:
        """Validate required configuration fields."""
        if not self.openai.api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in .env file or system environment."
            )

    def _validate_paths(self) -> None:
        """Validate and create required directories."""
        paths = [
            self.database.chromadb_path,
            self.database.persist_dir,
            os.path.dirname(self.logging.file) if self.logging.file else None,
        ]

        for path in paths:
            if path:
                Path(path).mkdir(parents=True, exist_ok=True)

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_level = getattr(logging, self.logging.level.upper(), logging.INFO)

        # Create logs directory if it doesn't exist
        if self.logging.file:
            log_dir = os.path.dirname(self.logging.file)
            Path(log_dir).mkdir(parents=True, exist_ok=True)

        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format=self.logging.format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.logging.file) if self.logging.file else None,
            ]
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "openai": self.openai.model_dump(),
            "playwright": self.playwright.model_dump(),
            "logging": self.logging.model_dump(),
            "database": self.database.model_dump(),
            "test_execution": self.test_execution.model_dump(),
            "api": self.api.model_dump(),
        }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global config instance
try:
    config = Config()
    logger.info("Configuration loaded successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


def reload_config() -> Config:
    """Reload configuration from environment."""
    global config
    config = Config()
    return config
