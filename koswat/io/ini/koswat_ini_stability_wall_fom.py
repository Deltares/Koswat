import math

from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniStabilityWallFom(FileObjectModelProtocol):
    storageFactorGround: str
    storageFactorConstruction: str
    storageFactorGroundPurchase: str
    steepeningInnerSlope: float
    minLenghtStabilityWall: float
    transitionSheetPileDeepWall: float
    maxLenghtStabilityWall: float

    def __init__(self) -> None:
        self.storageFactorGround = ""
        self.storageFactorConstruction = ""
        self.storageFactorGroundPurchase = ""
        self.steepeningInnerSlope = math.nan
        self.minLenghtStabilityWall = math.nan
        self.transitionSheetPileDeepWall = math.nan
        self.maxLenghtStabilityWall = math.nan

    def is_valid(self) -> bool:
        # TODO add validation
        #        check if values are initialized
        # how to test for an uninitialized bool?
        return (
            (self.storageFactorGround != "")
            & (self.storageFactorConstruction != "")
            & (self.storageFactorGroundPurchase != "")
            & (self.steepeningInnerSlope != math.nan)
            & (self.minLenghtStabilityWall != math.nan)
            & (self.transitionSheetPileDeepWall != math.nan)
            & (self.maxLenghtStabilityWall != math.nan)
        )
