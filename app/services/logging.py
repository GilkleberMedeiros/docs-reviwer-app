from dto.log_level import LOG_LEVEL_TYPE


class LEVEL:
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    INFO = "INFO"
    WARNING = "WARNING"


class Log:
    level: LOG_LEVEL_TYPE
    msg: str
    origin: str

    def __init__(self, level: LOG_LEVEL_TYPE, msg: str, origin: str) -> None:
        super().__init__()
        self.level = level
        self.msg = msg
        self.origin = origin

    def __str__(self) -> str:
        return f"{self.level} LOG {self.msg} FROM {self.origin}"

    def __repr__(self) -> str:
        return f"{self.level} LOG {self.msg} FROM {self.origin}"
