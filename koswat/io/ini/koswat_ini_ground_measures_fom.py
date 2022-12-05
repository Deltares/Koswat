import math

from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniGroundMeasuresFom(FileObjectModelProtocol):
    storageFactorGround: str
    storageFactorGroundPurchase: str
    minBankHeight: float
    maxBankHeightFactor: float
    factorGrowthBankHeight: float

    def __init__(self) -> None:
        self.storageFactorGround = ""
        self.storageFactorGroundPurchase = ""
        self.minBankHeight = math.nan
        self.maxBankHeightFactor = math.nan
        self.factorGrowthBankHeight = math.nan

    def is_valid(self) -> bool:
        # TODO add validation
        #        check if values are initialized
        # how to test for an uninitialized bool?
        return (
            (self.storageFactorGround != "")
            & (self.storageFactorGroundPurchase != "")
            & (self.minBankHeight != math.nan)
            & (self.maxBankHeightFactor != math.nan)
            & (self.factorGrowthBankHeight != math.nan)
        )
