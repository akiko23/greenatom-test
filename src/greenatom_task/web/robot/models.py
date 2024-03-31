from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column

from greenatom_task.web.database.base import Base


class Report(Base):  # type:ignore[misc]
    __tablename__ = 'robot_reports'

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column()
    duration: Mapped[timedelta] = mapped_column()

    # for the unit tests
    def __eq__(self, other: Base) -> bool:  # love mypy
        if not isinstance(other, Report):
            return NotImplemented
        return (
            self.id,
            self.started_at,
            self.duration
        ) == (other.id, other.started_at, other.duration)
