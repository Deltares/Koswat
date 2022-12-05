import math

from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniEnvironmentFom(FileObjectModelProtocol):
    environmentDatabases: str
    constructionDistance: float
    constructionTransfer: float
    unembanked: bool
    buildings: bool
    rail: bool
    water: bool

    def __init__(self) -> None:
        self.environmentDatabases = ""
        self.constructionDistance = math.nan
        self.constructionTransfer = math.nan
        self.unembanked = None
        self.buildings = None
        self.rail = None
        self.water = None

    def is_valid(self) -> bool:
        return (
            (self.environmentDatabases != "")
            & (self.constructionDistance != math.nan)
            & (self.constructionTransfer != math.nan)
            & (self.unembanked != None)
            & (self.buildings != None)
            & (self.rail != None)
            & (self.water != None)
        )
