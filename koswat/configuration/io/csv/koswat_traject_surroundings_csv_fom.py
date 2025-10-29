from __future__ import annotations
from dataclasses import dataclass, field

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class KoswatSurroundingsCsvFom(KoswatCsvFomProtocol):
    points_surroundings_list: list[PointSurroundings] = field(
        default_factory=lambda: []
    )
    traject: str = ""

    def is_valid(self) -> bool:
        return any(self.points_surroundings_list)
    
    def merge(self, other: KoswatSurroundingsCsvFom) -> None:
        """
        Merge another KoswatSurroundingsCsvFom into this one.

        Args:
            other (KoswatSurroundingsCsvFom): The other KoswatSurroundingsCsvFom to merge.

        Raises:
            ValueError: If the trajects of the two objects do not match.
        """
        if other.traject != self.traject:
            raise ValueError("Cannot merge surroundings fom with different trajects.")

        # Note: Suboptimal, but sufficient for now.
        _as_dict = {point.location: point for point in self.points_surroundings_list}
        for point in other.points_surroundings_list:
            if point.location not in _as_dict:
                self.points_surroundings_list.append(point)
            else:
                _as_dict[point.location].merge(point)