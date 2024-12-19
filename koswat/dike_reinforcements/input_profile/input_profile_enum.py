from enum import Enum


class InputProfileEnum(Enum):
    """
    Enum class for input profiles.
    """

    NONE = 0
    SOIL = 1
    VPS = 2
    PIPING_WALL = 3
    STABILITY_WALL = 4
    COFFERDAM = 5
