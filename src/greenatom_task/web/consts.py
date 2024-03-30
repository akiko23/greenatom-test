"""Contain all the project consts."""
from pathlib import Path

DEFAULT_CONFIG_PATH = '.configs/app.toml'
DEFAULT_PATH_TO_ROBOT_SCRIPT = Path(__file__).parent.parent.joinpath("robot", "robot_impl.py")
