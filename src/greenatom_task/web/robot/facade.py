"""
Facade is a design pattern which allows to interact with complex system/s via simple interface.
In this case the complex system is robot.
"""
import asyncio
import shlex
from asyncio.subprocess import Process
from typing import Optional

from greenatom_task.web.consts import DEFAULT_PATH_TO_ROBOT_SCRIPT
from greenatom_task.web.robot import exceptions


class RobotFacade:
    _robot_ps: Optional[Process] = None

    def __init__(self, robot_script_path: str = str(DEFAULT_PATH_TO_ROBOT_SCRIPT)) -> None:
        self.robot_script_path = robot_script_path

    async def start_robot(self, start: int = 0) -> None:
        if self._robot_ps and self._robot_ps.returncode is None:
            raise exceptions.RobotIsAlreadyRunning

        cmd = ["python", self.robot_script_path, "-s", str(start)]
        type(self)._robot_ps = await asyncio.create_subprocess_exec(*cmd)

    @classmethod
    async def stop_robot(cls) -> None:
        if not cls._robot_ps or cls._robot_ps.returncode is not None:
            raise exceptions.RobotIsInactive
        cls._robot_ps.kill()
        cls._robot_ps = None
