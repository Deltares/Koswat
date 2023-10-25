import logging
import math
from collections import defaultdict
from typing import Any, Type

from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.profile.volume_cost_parameters import VolumeCostParameter
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.strategies.strategy_location_matrix import StrategyLocationReinforcements


class SummaryMatrixCsvFomBuilder(BuilderProtocol):
    koswat_summary: KoswatSummary
    # Internal readonly properties.
    _volume_surface_key_column = "(volume / surface)"
    _cost_key_column = "(cost)"

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
        _csv_fom = KoswatCsvFom()

        _profile_type_key = "Profile type"
        _cost_per_km_key = "Cost per km (€)"
        _locations_key = "locations"

        _dict_of_entries = defaultdict(list)
        for _loc_prof_report in self.koswat_summary.locations_profile_report_list:
            _dict_of_entries[_profile_type_key].append(
                _loc_prof_report.profile_type_name
            )
            _dict_of_entries[_cost_per_km_key].append(_loc_prof_report.cost_per_km)
            self._get_volume_cost_parameters(
                _loc_prof_report.profile_cost_report.volume_cost_parameters.__dict__,
                _dict_of_entries,
            )
            # _dict_of_entries[_locations_key].append(_loc_prof_report.locations)

        if not _dict_of_entries:
            logging.error("No entries generated for the CSV Matrix.")
            return _csv_fom

        def dict_to_csv_row(key, placeholders: int) -> list[str]:
            row = _dict_of_entries[key]
            row.insert(0, key)
            for n in range(0, placeholders):
                row.insert(n, "")
            return row

        _location_rows = self._get_locations_matrix(
            self.koswat_summary.reinforcement_per_locations
        )
        _required_placeholders = 2  # Fix value.
        _headers = dict_to_csv_row(_profile_type_key, _required_placeholders)
        _cost_rows = [
            dict_to_csv_row(_parameter_key, _required_placeholders)
            for _parameter_key in _dict_of_entries.keys()
            if self._volume_surface_key_column in _parameter_key
            or self._cost_key_column in _parameter_key
        ]
        _cost_rows.insert(0, dict_to_csv_row(_cost_per_km_key, _required_placeholders))
        _csv_fom.headers = _headers
        _csv_fom.entries = _cost_rows + _location_rows
        return _csv_fom

    def _get_locations_matrix(
        self,
        reinforcement_per_locations: list[StrategyLocationReinforcements],
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
            _matrix[_reinforcement_per_location.location] = _suitable_locations + [
                _reinforcement_per_location.selected_measure.output_name
            ]

        return list(
            map(
                _location_as_row,
                sorted(_matrix.items(), key=lambda x: x[0].traject_order),
            )
        )

    def _get_volume_cost_parameters(
        self, vc_parameters: dict[str, VolumeCostParameter], csv_dictionary: dict
    ):
        def _format_parameter_name(dict_name: str) -> str:
            return dict_name.replace("_", " ").capitalize().strip()

        for (
            _parameter_name,
            _vc_parameter,
        ) in vc_parameters.items():
            _parameter_name = _format_parameter_name(_parameter_name)
            _volume_key = f"{_parameter_name} {self._volume_surface_key_column}:"
            csv_dictionary[_volume_key].append(
                _vc_parameter.volume if _vc_parameter else math.nan
            )

            _cost_key = f"{_parameter_name} {self._cost_key_column}:"
            csv_dictionary[_cost_key].append(
                _vc_parameter.total_cost() if _vc_parameter else math.nan
            )
