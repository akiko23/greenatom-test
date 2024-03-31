from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from greenatom_task.web.app_setup import (
    create_app,
    initialise_routers,
)
from greenatom_task.web.config import Config
from greenatom_task.web.depends_stub import Stub
from greenatom_task.web.robot.adapters import ReportRepository, RobotFacade
from greenatom_task.web.robot.dependencies import get_robot_service
from greenatom_task.web.robot.service import RobotService


@pytest.fixture(scope="function")
def config_mock() -> Mock:
    return Mock()


@pytest.fixture(scope="function")
def robot_facade_mock() -> AsyncMock:
    return AsyncMock()


@pytest.fixture(scope="function")
def report_repo_mock() -> AsyncMock:
    return AsyncMock()


@pytest.fixture(scope="function")
def app(config_mock: Mock):
    return create_app(config_mock)


@pytest.fixture(scope="function", autouse=True)
def init_routers(app: FastAPI):
    initialise_routers(app)


@pytest.fixture(scope="function", autouse=True)
def init_basic_dependencies(
        app: FastAPI,
        config_mock: Mock,
        robot_facade_mock: Mock,
        report_repo_mock: Mock
):
    session_mock = AsyncMock()

    app.dependency_overrides[Stub(AsyncSession)] = lambda: session_mock
    app.dependency_overrides[Stub(Config)] = lambda: config_mock
    app.dependency_overrides[Stub(RobotFacade)] = lambda: robot_facade_mock
    app.dependency_overrides[Stub(ReportRepository)] = lambda: report_repo_mock
    app.dependency_overrides[Stub(RobotService)] = get_robot_service


@pytest.fixture(scope="function")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
