"""Contain common dtos"""
from dataclasses import dataclass


@dataclass
class MsgResponse:
    """Represent a simple string message response.

    Attributes:
        msg (str): The message itself.
    """

    msg: str
