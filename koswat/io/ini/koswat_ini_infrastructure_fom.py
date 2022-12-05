import math

from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniInfrastructureFom(FileObjectModelProtocol):
    infrastructure: bool
    storageFactorRoads: str
    marginUnembanked: float
    roadsClass2Width: float
    roadsClass24Width: float
    roadsClass47Width: float
    roadsClass7Width: float
    roadsUnknownWidth: float

    def __init__(self) -> None:
        self.infrastructure = None
        self.storageFactorRoads = ""
        self.marginUnembanked = math.nan
        self.roadsClass2Width = math.nan
        self.roadsClass24Width = math.nan
        self.roadsClass47Width = math.nan
        self.roadsClass7Width = math.nan
        self.roadsUnknownWidth = math.nan

    def is_valid(self) -> bool:
        return (
            (self.infrastructure != None)
            & (self.storageFactorRoads != "")
            & (self.marginUnembanked != math.nan)
            & (self.roadsClass2Width != math.nan)
            & (self.roadsClass24Width != math.nan)
            & (self.roadsClass47Width != math.nan)
            & (self.roadsClass7Width != math.nan)
            & (self.roadsUnknownWidth != math.nan)
        )
