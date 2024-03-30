class RobotIsAlreadyRunning(Exception):
    def __str__(self) -> str:
        return "Robot is already running"


class RobotIsInactive(Exception):
    def __str__(self) -> str:
        return "Robot is inactive, so it cannot be stopped."
