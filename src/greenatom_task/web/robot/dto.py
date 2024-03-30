"""Contain common dtos"""
from datetime import datetime, timedelta

from pydantic import BaseModel


class ReportRead(BaseModel):
    id: int
    started_at: datetime
    duration: timedelta
