"""Contain functions required for configuration of the project components."""
from functools import partial

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from greenatom_task.web.config import AppConfig, Config, HttpServerConfig
from greenatom_task.web.database.dependencies import get_session
from greenatom_task.web.database.sa_utils import (
    create_engine,
    create_session_maker,
)
from greenatom_task.web.depends_stub import Stub
from greenatom_task.web.robot.adapters import ReportRepository, RobotFacade
from greenatom_task.web.robot.dependencies import (
    get_report_repository,
    get_robot_facade,
    get_robot_service,
)
from greenatom_task.web.robot.router import router as robot_router
from greenatom_task.web.robot.service import RobotService


def initialise_routers(app: FastAPI) -> None:
    """Include all routers to the app.

    Args:
        app (FastAPI): The FastAPI instance.
    """
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
    app.dependency_overrides[Stub(ReportRepository)] = get_report_repository
    app.dependency_overrides[Stub(RobotService)] = get_robot_service


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
