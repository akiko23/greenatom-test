"""Contain common dtos"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReportRead:
    id: int
    started_at: datetime
    finished_at: datetime
    duration: int  # duration in seconds
