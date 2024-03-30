"""Provide classes and functions for loading an application config."""
import logging
from dataclasses import dataclass

import toml

logger = logging.getLogger(__name__)

# You can replace this consts values with your own awesome ones :D
DEFAULT_APP_TITLE: str = 'greenatom-test'
DEFAULT_APP_DESCRIPTION: str = 'Greenatom test task'
DEFAULT_SERVER_HOST: str = '0.0.0.0'
DEFAULT_SERVER_PORT: int = 8000
DEFAULT_SERVER_LOG_LEVEL: str = 'info'


@dataclass(kw_only=True)  # type: ignore[call-overload]
class AppConfig:
    """Represent the application configuration.

    Attributes:
        title (str): The title of the application.
        description (str): The description of the application.
    """

    title: str = DEFAULT_APP_TITLE
    description: str = DEFAULT_APP_DESCRIPTION


@dataclass
class HttpServerConfig:
    """Represent the http server configuration.

    Attributes:
        host (str): The host of the server.
        port (int): The port of the server.
        log_level (str): The logging level of the server
    """

    host: str = DEFAULT_SERVER_HOST
    port: int = DEFAULT_SERVER_PORT
    log_level: str = DEFAULT_SERVER_LOG_LEVEL


@dataclass
class Database:
    """Represent the database configuration.

    Attributes:
        name (str): The name of the database.
    """
    name: str = "database.db"

    def __post_init__(self) -> None:
        """Initialise database URI."""
        self.uri = f"sqlite+aiosqlite:///{self.name}"


@dataclass
class Config:
    """Represent the overall configuration of the project.

    Attributes:
        app (AppConfig): The application configuration.
        http_server (HttpServerConfig): The HTTP server configuration.
        db (Database): The database configuration.
    """

    app: AppConfig
    http_server: HttpServerConfig
    db: Database


def load_config(config_path: str) -> Config:
    """Load configuration from a TOML file.

    Returns:
        Config: An instance of the Config class containing the loaded configuration.
    """
    with open(config_path, "r") as config_file:
        data = toml.load(config_file)
    return Config(
        app=AppConfig(**data["app"]),
        http_server=HttpServerConfig(**data["http_server"]),
        db=Database(**data["db"]),
    )
