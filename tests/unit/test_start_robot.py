from unittest.mock import AsyncMock, Mock

from starlette import status
from starlette.testclient import TestClient


def test_basic(client: TestClient, robot_facade_mock: AsyncMock):
    resp = client.post("robot/start")

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    expected_json = {"msg": "Robot was successfully started"}
    assert resp.json() == expected_json

    robot_facade_mock.start_robot.assert_called_once_with(start=0)


def test_with_query_param(client: TestClient, robot_facade_mock: Mock):
    start_number = 5
    resp = client.post("robot/start", params={"start": start_number})

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    expected_json = {"msg": "Robot was successfully started"}
    assert resp.json() == expected_json

    robot_facade_mock.start_robot.assert_called_once_with(start=start_number)


def test_when_robot_is_running(client: TestClient, robot_facade_mock: Mock):
    start_number = 5
    resp = client.post("robot/start", params={"start": start_number})

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    expected_json = {"msg": "Robot was successfully started"}
    assert resp.json() == expected_json

    robot_facade_mock.start_robot.assert_called_once_with(start=start_number)

