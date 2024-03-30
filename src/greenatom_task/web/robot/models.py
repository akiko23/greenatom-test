from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column

from greenatom_task.web.database.base import Base


class Report(Base):
    __tablename__ = 'robot_reports'

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column()
    duration: Mapped[timedelta] = mapped_column()
