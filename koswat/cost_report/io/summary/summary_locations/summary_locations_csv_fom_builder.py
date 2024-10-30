import logging
from collections import defaultdict
from typing import Any, Type

from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class SummaryLocationsCsvFomBuilder(BuilderProtocol):
    koswat_summary: KoswatSummary

    def __init__(self) -> None:
        self.koswat_summary = None

    def get_summary_reinforcement_type_column_order(
        self,
    ) -> list[Type[ReinforcementProfileProtocol]]:
        return [
            type(_report.profile_cost_report.reinforced_profile)
            for _report in self.koswat_summary.locations_profile_report_list
        ]

    def build(self) -> KoswatCsvFom:
        _ordered_profile_types = list(
            map(
                lambda x: x.profile_type_name,
                self.koswat_summary.locations_profile_report_list,
            )
        )

        return KoswatCsvFom(
            headers=(
                [
                    "Section",
                    "X coord",
                    "Y coord",
                ]
                + _ordered_profile_types
                + [
                    "Ordered selection",
                    "Optimized selection",
                ]
            ),
            entries=self._get_locations_matrix(
                self.koswat_summary.reinforcement_per_locations
            ),
        )

    def _get_locations_matrix(
        self,
        reinforcement_per_locations: list[StrategyLocationReinforcement],
    ) -> list[list[Any]]:
        def _location_as_row(
            matrix_item: tuple[PointSurroundings, list[int]]
        ) -> list[Any]:
            _ps, _m_values = matrix_item
            _location_as_row = [_ps.section, _ps.location.x, _ps.location.y]
            _location_as_row.extend(_m_values)
            return _location_as_row

        if not any(reinforcement_per_locations):
            logging.warning("No locations specified for the report.")
            return [[]]

        # Initiate locations matrix.
        _matrix = defaultdict(list)

        for _reinforcement_per_location in reinforcement_per_locations:
            _suitable_locations = [
                int(_type in _reinforcement_per_location.available_measures)
                for _type in self.get_summary_reinforcement_type_column_order()
            ]
            _matrix[_reinforcement_per_location.location] = _suitable_locations + list(
                map(
                    lambda x: x.output_name,
                    _reinforcement_per_location.output_selected_measures(2),
                )
            )

        return list(
            map(
                _location_as_row,
                sorted(_matrix.items(), key=lambda x: x[0].traject_order),
            )
        )
