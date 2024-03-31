from datetime import date, time
from unittest.mock import AsyncMock

from starlette import status
from starlette.testclient import TestClient

from greenatom_task.web.robot.dto import ReportRead


def test_basic(client: TestClient, report_repo_mock: AsyncMock):
    reports = [
        ReportRead(
            id=1,
            started_at=time(hour=12, minute=40, second=12),
            finished_at=time(hour=12, minute=40, second=59),
            duration=47,
            count_start_date=date(
                year=2024,
                month=3,
                day=31,
            ),
        ),
        ReportRead(
            id=2,
            started_at=time(hour=12, minute=40, second=12),
            finished_at=time(hour=12, minute=40, second=59),
            duration=47,
            count_start_date=date(
                year=2024,
                month=3,
                day=31,
            ),
        )
    ]
    report_repo_mock.get_all.return_value = reports

    resp = client.get("robot/reports")

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    # 🫠
    expected_json = [
        {
            k: str(getattr(r, k))
            if isinstance(getattr(r, k), date | time)
            else getattr(r, k)
            for k in r.__annotations__
        } for r in reports
    ]
    assert resp.json() == expected_json


def test_no_reports(client: TestClient, report_repo_mock: AsyncMock):
    report_repo_mock.get_all.return_value = []

    resp = client.get("robot/reports")

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    assert resp.json() == []
