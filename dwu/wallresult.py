from enum import Enum, auto

class WallResult(Enum):
    TODAY = auto()
    MOST_RECENT = auto()
    ALREADY_SET = auto()
    SET = auto()
    NO_VALID = auto()
