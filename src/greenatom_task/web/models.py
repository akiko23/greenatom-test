from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column

from greenatom_task.database.base import Base


class Reports(Base):  # type:ignore[misc]
    __tablename__ = 'reports'

    started_at: Mapped[datetime] = mapped_column()
    duration: Mapped[timedelta] = mapped_column()
