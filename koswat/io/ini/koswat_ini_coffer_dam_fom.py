import math

from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniCofferDamFom(FileObjectModelProtocol):
    storageFactorGround: str
    storageFactorConstruction: str
    minLenghtCofferDam: float
    maxLenghtCofferDam: float

    def __init__(self) -> None:
        self.storageFactorGround = ""
        self.storageFactorConstruction = ""
        self.minLenghtCofferDam = math.nan
        self.maxLenghtCofferDam = math.nan

    def is_valid(self) -> bool:
        return (
            (self.storageFactorGround != "")
            & (self.storageFactorConstruction != "")
            & (self.minLenghtCofferDam != math.nan)
            & (self.maxLenghtCofferDam != math.nan)
        )
