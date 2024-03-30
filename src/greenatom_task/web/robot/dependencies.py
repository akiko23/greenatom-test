from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from greenatom_task.web.depends_stub import Stub
from greenatom_task.web.robot.adapters import ReportRepository, RobotFacade
from greenatom_task.web.robot.service import RobotService


def get_robot_facade() -> RobotFacade:
    return RobotFacade()


def get_report_repository(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> ReportRepository:
    return ReportRepository(session=session)


def get_robot_service(
        robot_facade: RobotFacade = Depends(Stub(RobotFacade)),
        report_repo: ReportRepository = Depends(Stub(ReportRepository)),
) -> RobotService:
    return RobotService(robot_facade=robot_facade, report_repo=report_repo)
