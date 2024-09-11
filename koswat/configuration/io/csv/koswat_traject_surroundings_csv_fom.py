from dataclasses import dataclass, field

from koswat.configuration.io.csv.koswat_point_surroundings_fom import (
    KoswatPointSurroundingsFom,
)
from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


@dataclass
class KoswatTrajectSurroundingsCsvFom(KoswatCsvFomProtocol):
    points_surroundings_list: list[KoswatPointSurroundingsFom] = field(
        default_factory=lambda: []
    )
    distances_list: list[float] = field(default_factory=lambda: [])
    traject: str = ""

    def is_valid(self) -> bool:
        return self.points_surroundings_list and any(self.points_surroundings_list)
