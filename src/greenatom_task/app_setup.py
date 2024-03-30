"""Contain functions required for configuration of the project components."""


import uvicorn
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from greenatom_task.config import AppConfig, Config, HttpServerConfig
from greenatom_task.depends_stub import Stub

router = APIRouter()


class MsgResponse(BaseModel):
    """Represent a simple string message response.

    Attributes:
        msg (str): The message itself.
    """

    msg: str


@router.get('/')
async def read_main() -> MsgResponse:
    """Read the root endpoint (Only in testing purposes).

    Returns:
        MsgResponse: The message response instance.
    """
    return MsgResponse(msg='Welcome to Sirius-journal API!')


def initialise_routers(app: FastAPI) -> None:
    """Include all routers to the app.

    Args:
        app (FastAPI): The FastAPI instance.
    """
    app.include_router(router)


def initialise_dependencies(app: FastAPI, config: Config) -> None:
    """Initialise the dependencies in the app.

    Args:
        app (FastAPI): The FastAPI instance.
        config (Config): The config instance.
    """
    app.dependency_overrides[Stub(Config)] = lambda: config


def create_app(app_cfg: AppConfig) -> FastAPI:
    """Creates a FastAPI instance.

    Args:
        app_cfg (AppConfig): The app configuration.

    Returns:
        FastAPI: The created FastAPI instance.
    """
    app = FastAPI(title=app_cfg.title, description=app_cfg.description)
    return app


def create_http_server(app: FastAPI, http_server_cfg: HttpServerConfig) -> uvicorn.Server:
    """Creates uvicorn HTTP server instance.

    Args:
        app (FastAPI): The FastAPI instance.
        http_server_cfg (HttpServerConfig): The HTTP server configuration.

    Returns:
        uvicorn.Server: The created Uvicorn server instance.
    """
    uvicorn_config = uvicorn.Config(
        app,
        host=http_server_cfg.host,
        port=http_server_cfg.port,
        log_level=http_server_cfg.log_level,
    )
    return uvicorn.Server(uvicorn_config)
