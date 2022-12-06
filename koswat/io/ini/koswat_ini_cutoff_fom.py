import math

from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniCutoffFom(FileObjectModelProtocol):
    storageFactorGround: str
    storageFactorConstruction: str
    storageFactorGroundPurchase: str
    minLenghtCutoff: float
    transitionCBWallSheetPile: int
    maxLenghtCutoff: float

    def __init__(self) -> None:
        self.storageFactorGround = ""
        self.storageFactorConstruction = ""
        self.storageFactorGroundPurchase = ""
        self.minLenghtCutoff = math.nan
        self.transitionCBWallSheetPile = math.nan
        self.maxLenghtCutoff = math.nan

    def is_valid(self) -> bool:
        return (
            (self.storageFactorGround != "")
            & (self.storageFactorGroundPurchase != "")
            & (self.minLenghtCutoff != math.nan)
            & (self.transitionCBWallSheetPile != math.nan)
            & (self.maxLenghtCutoff != math.nan)
        )
