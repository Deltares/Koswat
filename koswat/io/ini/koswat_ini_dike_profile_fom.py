import math

from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniDikeProfileFom(FileObjectModelProtocol):
    thicknessGrassLayer: float
    thicknessClayLayer: float

    def __init__(self) -> None:
        self.thicknessClayLayer = math.nan
        self.thicknessGrassLayer = math.nan

    def is_valid(self) -> bool:
        # TODO add validation
        #        check if values are initialized
        # how to test for an uninitialized bool?
        return (self.thicknessGrassLayer != math.nan) & (
            self.thicknessClayLayer != math.nan
        )
