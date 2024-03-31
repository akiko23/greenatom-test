from datetime import datetime
from unittest.mock import AsyncMock, PropertyMock

from starlette import status
from starlette.testclient import TestClient

from greenatom_task.web.robot.models import Report


def test_basic(client: TestClient, robot_facade_mock: AsyncMock, report_repo_mock: AsyncMock):
    started_at, duration = datetime.now(), 10

    # imitating active robot process
    robot_ps_mock = PropertyMock()
    robot_facade_mock.robot_ps = robot_ps_mock
    robot_ps_mock.returncode = None

    robot_facade_mock.get_last_launch_data.return_value = (started_at, duration)

    resp = client.post("robot/stop")

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    expected_json = {"msg": "Robot was successfully stopped"}
    assert resp.json() == expected_json

    robot_facade_mock.stop_robot.assert_called_once()
    robot_facade_mock.get_last_launch_data.assert_called_once()
    report_repo_mock.create.assert_called_once_with(
        Report(
            started_at=started_at,
            duration=duration,
        )
    )


def test_when_robot_is_inactive(client: TestClient, robot_facade_mock: AsyncMock):
    # imitating inactive robot process
    robot_ps_mock = PropertyMock(return_value=None)
    robot_facade_mock.robot_ps = robot_ps_mock

    resp = client.post("robot/stop")

    expected_status = status.HTTP_400_BAD_REQUEST
    assert resp.status_code == expected_status

    expected_json = {"detail": "Robot is inactive, so it cannot be stopped."}
    assert resp.json() == expected_json

#
# def test_when_robot_is_running(client: TestClient, robot_facade_mock: Mock):
#     start_number = 5
#     resp = client.post("robot/start", params={"start": start_number})
#
#     expected_status = status.HTTP_200_OK
#     assert resp.status_code == expected_status
#
#     expected_json = {"msg": "Robot was successfully started"}
#     assert resp.json() == expected_json
#
#     robot_facade_mock.start_robot.assert_called_once_with(start=start_number)
