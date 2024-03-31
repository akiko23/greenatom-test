"""Contain common dtos"""
from dataclasses import dataclass
from datetime import date, time


@dataclass
class ReportRead:
    id: int
    started_at: time
    finished_at: time
    duration: int  # duration in seconds
    count_start_date: date
