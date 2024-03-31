import pytest
from httpx import AsyncClient
from starlette import status

from greenatom_task.web.robot.adapters import RobotFacade


@pytest.mark.asyncio
async def test_basic(client: AsyncClient, robot_facade: RobotFacade):
    # preparation
    await robot_facade.start_robot()

    resp = await client.post("robot/stop")

    expected_status = status.HTTP_200_OK
    assert resp.status_code == expected_status

    expected_json = {"msg": "Robot was successfully stopped"}
    assert resp.json() == expected_json


@pytest.mark.asyncio
async def test_when_robot_is_inactive(client: AsyncClient):
    resp = await client.post("robot/stop")

    expected_status = status.HTTP_400_BAD_REQUEST
    assert resp.status_code == expected_status

    expected_json = {"detail": "Robot is inactive, so it cannot be stopped."}
    assert resp.json() == expected_json
