"""Configuration settings for app.

This module uses pydantic-settings to manage environment variables with
validation and type checking.
"""

from pathlib import Path
from typing import Literal, Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSettings(BaseSettings):
    """Application settings loaded from environment variables.

    IMPORTANT: When adding new settings, also update:
    - .env.example with the new variable
    - README.md Configuration > Environment Variables section

    Attributes:
        debug: Enable debug mode
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        api_host: API host address
        api_port: API port number
    """

    model_config: SettingsConfigDict = SettingsConfigDict(  # pyright: ignore[reportIncompatibleVariableOverride]
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Deployment
    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )

    api_host: str = Field(
        default="0.0.0.0",
        description="API host address",
    )

    api_port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="API port number",
    )

    cwd: Path | None = Field(
        default=None,
        description="Current working directory (absolute path)",
    )

    logs_dir: str = Field(  # pyright: ignore[reportAssignmentType, reportRedeclaration]
        default="logs",
        description="Directory for log files (relative to cwd)",
    )

    data_dir: str = Field(  # pyright: ignore[reportAssignmentType, reportRedeclaration]
        default="data",
        description="Directory for data files (relative to cwd)",
    )

    @model_validator(mode="after")
    def validate_fields(self) -> Self:
        assert self.cwd

        self.data_dir: Path = self.cwd / self.data_dir
        self.logs_dir: Path = self.cwd / self.logs_dir

        for directory in [self.data_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        return self


# Global settings instance
env_settings = EnvironmentSettings()
