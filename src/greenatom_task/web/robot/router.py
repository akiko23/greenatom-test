"""Handlers for the 'robot' resource."""
from fastapi import APIRouter, Depends, HTTPException, status

from greenatom_task.web.depends_stub import Stub
from greenatom_task.web.dto import MsgResponse
from greenatom_task.web.robot import exceptions
from greenatom_task.web.robot.facade import RobotFacade

router = APIRouter(prefix="/robot", tags=["robot"])


@router.post("/start")
async def start_robot(
        start: int = 0,
        robot_facade: RobotFacade = Depends(Stub(RobotFacade))
) -> MsgResponse:
    try:
        await robot_facade.start_robot(start=start)
    except exceptions.RobotIsAlreadyRunning as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return MsgResponse(msg="Robot was successfully started")


@router.post("/stop")
async def stop_robot(robot_facade: RobotFacade = Depends(Stub(RobotFacade))) -> MsgResponse:
    try:
        await robot_facade.stop_robot()
    except exceptions.RobotIsInactive as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return MsgResponse(msg="Robot was successfully stopped")
