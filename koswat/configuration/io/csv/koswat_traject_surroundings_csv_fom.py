from dataclasses import dataclass, field

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class KoswatSurroundingsCsvFom(KoswatCsvFomProtocol):
    points_surroundings_list: list[PointSurroundings] = field(
        default_factory=lambda: []
    )
    distances_list: list[float] = field(default_factory=lambda: [])
    traject: str = ""

    def is_valid(self) -> bool:
        return any(self.points_surroundings_list)
