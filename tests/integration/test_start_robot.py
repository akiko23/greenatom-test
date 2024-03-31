import pytest
from httpx import AsyncClient
from starlette import status

from greenatom_task.web.robot.adapters import RobotFacade


@pytest.mark.asyncio
async def test_basic(client: AsyncClient, robot_facade: RobotFacade):
    resp = await client.post("robot/start")

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    expected_json = {"msg": "Robot was successfully started"}
    assert resp.json() == expected_json

    # finalization
    await robot_facade.stop_robot()


@pytest.mark.asyncio
async def test_with_query_param(client: AsyncClient, robot_facade: RobotFacade):
    start_number = 5
    resp = await client.post("robot/start", params={"start": start_number})

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    expected_json = {"msg": "Robot was successfully started"}
    assert resp.json() == expected_json

    # reading from robot stdout
    with open("robot_logs", "r", encoding="utf-8") as f:
        start_from_stdout = int(f.readline().split()[0])

    assert start_from_stdout == start_number

    # finalization
    await robot_facade.stop_robot()


@pytest.mark.asyncio
async def test_when_robot_is_running(client: AsyncClient, robot_facade: RobotFacade):
    # preparation
    await robot_facade.start_robot()

    resp = await client.post("robot/start")

    expected_status = status.HTTP_400_BAD_REQUEST
    assert resp.status_code == expected_status

    expected_json = {"detail": "Robot is already running"}
    assert resp.json() == expected_json

    # finalization
    await robot_facade.stop_robot()
