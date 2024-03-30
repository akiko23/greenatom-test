"""Contain functions required for configuration of the project components."""
from functools import partial

import uvicorn
from fastapi import APIRouter, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from greenatom_task.web.config import AppConfig, Config, HttpServerConfig
from greenatom_task.web.database.dependencies import get_session
from greenatom_task.web.database.sa_utils import create_session_maker, create_engine
from greenatom_task.web.depends_stub import Stub
from greenatom_task.web.dto import MsgResponse
from greenatom_task.web.robot.dependencies import get_robot_facade
from greenatom_task.web.robot.facade import RobotFacade
from greenatom_task.web.robot.router import router as robot_router

router = APIRouter()


@router.get('/')
async def read_main() -> MsgResponse:
    """Read the root endpoint (Only in testing purposes).

    Returns:
        MsgResponse: The message response instance.
    """
    return MsgResponse(msg='Welcome to API for an interaction with robot!')


def initialise_routers(app: FastAPI) -> None:
    """Include all routers to the app.

    Args:
        app (FastAPI): The FastAPI instance.
    """
    app.include_router(router)
    app.include_router(robot_router)


def initialise_dependencies(app: FastAPI, config: Config) -> None:
    """Initialise the dependencies in the app.

    Args:
        app (FastAPI): The FastAPI instance.
        config (Config): The config instance.
    """
    engine = create_engine(config.db.uri)
    session_factory = create_session_maker(engine)

    app.dependency_overrides[Stub(AsyncSession)] = partial(get_session, session_factory)
    app.dependency_overrides[Stub(Config)] = lambda: config
    app.dependency_overrides[Stub(RobotFacade)] = get_robot_facade


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
