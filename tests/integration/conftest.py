from typing import AsyncGenerator, TypeAlias

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from greenatom_task.web.app_setup import (
    create_app,
    initialise_dependencies,
    initialise_routers,
)
from greenatom_task.web.config import Config, load_config
from greenatom_task.web.database.base import Base
from greenatom_task.web.database.sa_utils import (
    create_session,
    create_session_maker,
)
from greenatom_task.web.depends_stub import Stub
from greenatom_task.web.robot.adapters import ReportRepository, RobotFacade
from greenatom_task.web.robot.models import Report  # noqa

BASE_URL = "http://test"
TEST_CONFIG_PATH = ".configs/test.toml"
MIGRATIONS_PATH = "src/greenatom_task/web/migrations"

SessionMaker: TypeAlias = sessionmaker[AsyncSession]


@pytest.fixture(scope="function")
def config() -> Config:
    return load_config(TEST_CONFIG_PATH)


@pytest.fixture(scope="function")
def db_url(config: Config) -> str:
    return config.db.uri


@pytest.fixture(scope="function")
def engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url, echo=True)


@pytest.fixture(scope="function")
def session_factory(engine: AsyncEngine) -> SessionMaker:
    session_maker = create_session_maker(engine)
    return session_maker


@pytest_asyncio.fixture(scope="function")
async def session(
        session_factory: SessionMaker,
) -> AsyncGenerator[AsyncSession, None]:
    async with create_session(session_factory) as async_session:
        yield async_session


@pytest.fixture(scope="function")
def report_repo(session: AsyncSession) -> ReportRepository:
    return ReportRepository(session=session)


@pytest.fixture(scope="function")
def robot_facade() -> RobotFacade:
    return RobotFacade()


@pytest.fixture(scope="function")
def app(config: Config, robot_facade: RobotFacade, report_repo: ReportRepository) -> FastAPI:
    app = create_app(config.app)
    initialise_routers(app)
    initialise_dependencies(app, config)

    # override robot facade
    app.dependency_overrides[Stub(RobotFacade)] = lambda: robot_facade
    app.dependency_overrides[Stub(ReportRepository)] = lambda: report_repo

    return app


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI, config: Config) -> AsyncClient:
    async with AsyncClient(
            app=app,
            base_url=config.http_server.host,
            headers={"Accept": "application/json"},
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="function", autouse=True)
async def initialise_migrations(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
