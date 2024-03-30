"""The business logic layer. Yeah, it is :)"""

from greenatom_task.web.robot import exceptions
from greenatom_task.web.robot.adapters import ReportRepository, RobotFacade
from greenatom_task.web.robot.models import Report


class RobotService:

    def __init__(
            self,
            robot_facade: RobotFacade,
            report_repo: ReportRepository,
    ) -> None:
        self.robot_facade = robot_facade
        self.report_repo = report_repo

    async def start_robot(self, start: int = 0) -> None:
        robot_ps = self.robot_facade.robot_ps
        if robot_ps and robot_ps.returncode is None:
            raise exceptions.RobotIsAlreadyRunning

        await self.robot_facade.start_robot(start)

    async def stop_robot(self) -> None:
        robot_ps = self.robot_facade.robot_ps
        if not robot_ps or robot_ps.returncode is not None:
            raise exceptions.RobotIsInactive

        self.robot_facade.stop_robot()

        started_at, duration = self.robot_facade.get_last_launch_data()
        await self.report_repo.create(Report(started_at=started_at, duration=duration))

    async def get_robot_reports(self) -> list[Report]:
        reports: list[Report] = await self.report_repo.get_all()
        return reports
