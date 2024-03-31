import asyncio
from asyncio.subprocess import Process
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from greenatom_task.web.consts import DEFAULT_PATH_TO_ROBOT_SCRIPT
from greenatom_task.web.robot.dto import ReportRead
from greenatom_task.web.robot.models import Report


class ReportRepository:
    """Adapter to data layer of the robot reports."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, report: Report) -> None:
        self.session.add(report)
        await self.session.commit()

    async def get_all(self) -> list[ReportRead]:
        stmt = select(Report)
        reports = await self.session.scalars(stmt)

        return [
            ReportRead(
                id=report.id,
                started_at=report.started_at,
                finished_at=report.started_at + report.duration,
                duration=report.duration.total_seconds(),
            )
            for report in reports.all()
        ]


class RobotFacade:
    """
    Facade is a design pattern which allows
    to interact with complex system/s via simple interface.

    In this case the complex system is robot.
    """

    started_at: Optional[datetime] = None
    _robot_ps: Optional[Process] = None

    def __init__(
            self,
            robot_script_path: str = str(DEFAULT_PATH_TO_ROBOT_SCRIPT)
    ) -> None:
        self.robot_script_path = robot_script_path

    @property
    def robot_ps(self) -> Optional[Process]:
        return self._robot_ps

    async def start_robot(self, start: int = 0) -> None:
        cmd = ["python", self.robot_script_path, "-s", str(start)]
        type(self).started_at = datetime.now()
        type(self)._robot_ps = await asyncio.create_subprocess_exec(*cmd)

    @classmethod
    def stop_robot(cls) -> None:
        cls._robot_ps.kill()  # type:ignore[union-attr]
        cls._robot_ps = None

    @classmethod
    def get_last_launch_data(cls) -> tuple[datetime, int]:
        with open("robot_logs", "r", encoding="utf-8") as f:
            output = f.readline().split()

        start, end = int(output[0]), int(output[-1])
        duration = end - start

        return cls.started_at, timedelta(seconds=duration)  # type:ignore[return-value]
