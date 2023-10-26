import logging
from typing import Type

from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class KoswatSummaryLocationMatrixBuilder(BuilderProtocol):
    """
    NOTE: Although this 'problem' could be easily solved with `pandas`
    or `numpy`, I prefer not to include external (heavy) dependencies unless
    strictily necessary.
    If / when performance would become a problem, then this builder could (perhaps)
    benefit from using the aforementioned libraries.
    """

    locations_profile_report_list: list[MultiLocationProfileCostReport]
    available_locations: list[PointSurroundings]

    def _get_multi_location_profile_to_dict_matrix(
        self, locations_profile: MultiLocationProfileCostReport
    ) -> dict[PointSurroundings, Type[ReinforcementProfileProtocol]]:
        return dict(
            (_location, type(locations_profile.profile_cost_report.reinforced_profile))
            for _location in locations_profile.locations
        )

    def _get_list_summary_matrix_for_locations_with_reinforcements(
        self,
    ) -> list[dict[PointSurroundings, Type[ReinforcementProfileProtocol]]]:
        return list(
            map(
                self._get_multi_location_profile_to_dict_matrix,
                self.locations_profile_report_list,
            )
        )

    def build(
        self,
    ) -> dict[PointSurroundings, list[Type[ReinforcementProfileProtocol]]]:
        # 1. First we get all the possible reinforcements per point.

        logging.info("Initalizing locations-reinforcements matrix.")
        _reinforce_matrix_dict_list = (
            self._get_list_summary_matrix_for_locations_with_reinforcements()
        )

        # 2. Then we initialize the matrix with all available locations,
        # but no reinforcements.

        _summary_matrix = dict((_ps, []) for _ps in self.available_locations)

        # 3. Last, we merge the reinforcements dictionary into the matrix.
        for _location in _summary_matrix.keys():
            for _reinforce_matrix_dict in _reinforce_matrix_dict_list:
                if _location in _reinforce_matrix_dict:
                    _summary_matrix[_location].append(_reinforce_matrix_dict[_location])

        # 4. Sort matrix by traject order for normalized usage in Koswat.
        _summary_matrix = dict(
            sorted(_summary_matrix.items(), key=lambda x: x[0].traject_order)
        )

        logging.info("Finalized locations-reinforcements matrix.")

        return _summary_matrix
