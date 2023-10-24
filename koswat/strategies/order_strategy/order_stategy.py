from koswat.cost_report.summary.koswat_summary_location_matrix import (
    KoswatSummaryLocationMatrix,
)

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
)


class OrderStrategy:
    _location_matrix: KoswatSummaryLocationMatrix

    def __init__(self, locations_matrix: KoswatSummaryLocationMatrix) -> None:
        self._location_matrix = locations_matrix

    def get_locations_reinforcements(
        self,
    ) -> dict[PointSurroundings, ReinforcementProfile]:
        raise NotImplementedError()
