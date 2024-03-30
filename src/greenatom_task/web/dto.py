"""Contain common dtos"""
from pydantic import BaseModel


class MsgResponse(BaseModel):
    """Represent a simple string message response.

    Attributes:
        msg (str): The message itself.
    """

    msg: str
