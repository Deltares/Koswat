import logging
import math
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.profile.volume_cost_parameters import VolumeCostParameter
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class SummaryMatrixCsvFomBuilder(BuilderProtocol):
    koswat_summary: KoswatSummary
    # Internal readonly properties.
    _volume_surface_key_column = "(volume / surface)"
    _cost_key_column = "(cost)"

    def __init__(self) -> None:
        self.koswat_summary = None

    def build(self) -> KoswatCsvFom:
        _csv_fom = KoswatCsvFom()

        _profile_type_key = "Profile type"
        _cost_per_km_key = "Cost per km (€)"
        _locations_key = "locations"

        _dict_of_entries = defaultdict(list)
        for _loc_prof_report in self.koswat_summary.locations_profile_report_list:
            _dict_of_entries[_profile_type_key].append(_loc_prof_report.profile_type)
            _dict_of_entries[_cost_per_km_key].append(_loc_prof_report.cost_per_km)
            self._get_volume_cost_parameters(
                _loc_prof_report.profile_cost_report.volume_cost_parameters.__dict__,
                _dict_of_entries,
            )
            _dict_of_entries[_locations_key].append(_loc_prof_report.locations)

        if not _dict_of_entries:
            logging.error("No entries generated for the CSV Matrix.")
            return _csv_fom

        def dict_to_csv_row(key, placeholders: int) -> List[str]:
            row = _dict_of_entries[key]
            row.insert(0, key)
            for n in range(0, placeholders):
                row.insert(n, "")
            return row

        _location_rows = self._get_locations_matrix(_dict_of_entries[_locations_key])
        _required_placeholders = (
            len(_location_rows[0])
            - len(self.koswat_summary.locations_profile_report_list)
            - 1
        )
        _headers = dict_to_csv_row(_profile_type_key, _required_placeholders)
        _cost_rows = [
            dict_to_csv_row(_parameter_key, _required_placeholders)
            for _parameter_key in _dict_of_entries.keys()
            if self._volume_surface_key_column in _parameter_key
            or self._cost_key_column in _parameter_key
        ]
        _cost_rows.insert(0, dict_to_csv_row(_cost_per_km_key, _required_placeholders))
        _csv_fom.headers = _headers
        _csv_fom.entries = _location_rows + _cost_rows
        return _csv_fom

    def _get_locations_matrix(
        self, locations_lists: List[List[PointSurroundings]]
    ) -> List[List[Any]]:
        def location_as_row(
            matrix_item: Tuple[PointSurroundings, List[int]]
        ) -> List[Any]:
            _ps, _m_values = matrix_item
            _location_as_row = [_ps.section, _ps.location.x, _ps.location.y]
            _location_as_row.extend(_m_values)
            return _location_as_row

        _matrix = defaultdict(list)
        for idx, _loc_list in enumerate(locations_lists):
            for _loc in _loc_list:
                if not _matrix[_loc]:
                    _matrix[_loc] = [0] * len(locations_lists)
                _matrix[_loc][idx] = 1
        return list(
            map(
                location_as_row,
                sorted(_matrix.items(), key=lambda x: x[0].traject_order),
            )
        )

    def _get_volume_cost_parameters(
        self, vc_parameters: Dict[str, VolumeCostParameter], csv_dictionary: dict
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
