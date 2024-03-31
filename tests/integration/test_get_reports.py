import asyncio
from datetime import datetime

import pytest
from httpx import AsyncClient
from starlette import status

from greenatom_task.web.robot.adapters import ReportRepository
from greenatom_task.web.robot.models import Report
from greenatom_task.web.robot.service import RobotService


@pytest.mark.asyncio
async def test_basic(
        client: AsyncClient,
        robot_facade: RobotService,
        report_repo: ReportRepository
):
    # run robot couple of times
    number_of_reports = 2
    for _ in range(number_of_reports):
        started_at = datetime.now()

        await robot_facade.start_robot(start=5)
        await asyncio.sleep(2)
        await robot_facade.stop_robot()

        duration = datetime.now() - started_at
        await report_repo.create(report=Report(
            started_at=started_at,
            duration=duration,
        ))

    resp = await client.get("robot/reports")

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    assert len(resp.json()) == number_of_reports


@pytest.mark.asyncio
async def test_no_reports(client: AsyncClient):
    resp = await client.get("robot/reports")

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    assert resp.json() == []
