import logging
import math
from collections import defaultdict
from itertools import groupby
from typing import Type

from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.profile.quantity_cost_parameters import CostParameterProtocol
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class SummaryCostsCsvFomBuilder(BuilderProtocol):
    koswat_summary: KoswatSummary
    # Internal readonly properties.
    _quantity_key_column = "(quantity)"
    _cost_key_column = "(cost)"
    _cost_with_surtax_key_column = "(cost incl surtax)"
    _decimals = 2

    def __init__(self) -> None:
        self.koswat_summary = None

    @staticmethod
    def dict_to_csv_row(csv_to_convert: dict) -> list[list[str]]:
        return [
            [_parameter_key] + _param_values
            for _parameter_key, _param_values in csv_to_convert.items()
        ]

    def build(self) -> KoswatCsvFom:
        _csv_fom = KoswatCsvFom()

        _profile_type_key = "Profile type"
        _cost_per_km_key = "Cost per km (Euro/km)"
        _cost_per_km_incl_surtax_key = "Cost per km incl surtax (Euro/km)"

        _dict_of_entries = defaultdict(list)
        for _loc_prof_report in self.koswat_summary.locations_profile_report_list:
            _dict_of_entries[_profile_type_key].append(
                _loc_prof_report.profile_type_name
            )
            _dict_of_entries[_cost_per_km_key].append(_loc_prof_report.cost_per_km)
            _dict_of_entries[_cost_per_km_incl_surtax_key].append(
                _loc_prof_report.cost_per_km_with_surtax
            )
            self._get_quantity_cost_parameters(
                _loc_prof_report.profile_cost_report.quantity_cost_parameters.__dict__,
                _dict_of_entries,
            )

        if not _dict_of_entries:
            logging.error("No entries generated for the CSV Matrix.")
            return _csv_fom

        _cost_per_km_rows = [
            [_cost_per_km_key] + _dict_of_entries[_cost_per_km_key],
            [_cost_per_km_incl_surtax_key]
            + _dict_of_entries[_cost_per_km_incl_surtax_key],
        ]
        _quantity_costs_rows = self.dict_to_csv_row(
            dict(
                filter(
                    lambda x: self._quantity_key_column in x[0]
                    or self._cost_key_column in x[0]
                    or self._cost_with_surtax_key_column in x[0],
                    _dict_of_entries.items(),
                )
            ),
        )
        _selected_measure_cost_rows = self.dict_to_csv_row(
            self._get_cost_per_selected_measure()
        )

        _csv_fom.headers = [_profile_type_key] + _dict_of_entries[_profile_type_key]
        _csv_fom.entries = (
            _cost_per_km_rows + _quantity_costs_rows + _selected_measure_cost_rows
        )
        return _csv_fom

    def _get_total_meters_per_selected_measure(
        self,
    ) -> dict[ReinforcementProfileProtocol, int]:
        # We consider the distance between adjacent locations
        # ALWAYS to be of 1 meter.
        _sorted_reinforcements = sorted(
            self.koswat_summary.reinforcement_per_locations,
            key=lambda x: x.selected_measure.output_name,
        )
        return dict(
            (k, len(list(g)))
            for k, g in groupby(
                _sorted_reinforcements,
                lambda x: x.selected_measure,
            )
        )

    def _get_summary_reinforcement_type_column_order(
        self,
    ) -> list[Type[ReinforcementProfileProtocol]]:
        return [
            type(_report.profile_cost_report.reinforced_profile)
            for _report in self.koswat_summary.locations_profile_report_list
        ]

    def _get_cost_per_selected_measure(self) -> dict:
        _total_measure_meters_key = "Total measure meters"
        _total_measure_cost_key = "Total measure cost"
        _total_measure_cost_incl_surtax_key = "Total measure cost incl surtax"
        _selected_measures_rows = defaultdict(list)
        _total_meters_per_selected_measure = (
            self._get_total_meters_per_selected_measure()
        )
        for _ordered_reinf in self._get_summary_reinforcement_type_column_order():
            _total_meters = _total_meters_per_selected_measure.get(_ordered_reinf, 0)
            _selected_measures_rows[_total_measure_meters_key].append(_total_meters)

            _report_by_profile = self.koswat_summary.get_report_by_profile(
                _ordered_reinf
            )
            _total_cost = _total_meters * _report_by_profile.cost_per_km / 1000
            _selected_measures_rows[_total_measure_cost_key].append(_total_cost)

            _total_cost_with_surtax = (
                _total_meters * _report_by_profile.cost_per_km_with_surtax / 1000
            )
            _selected_measures_rows[_total_measure_cost_incl_surtax_key].append(
                _total_cost_with_surtax
            )

        _selected_measures_rows[_total_measure_cost_key].append(
            sum(_selected_measures_rows[_total_measure_cost_key])
        )
        _selected_measures_rows[_total_measure_cost_incl_surtax_key].append(
            sum(_selected_measures_rows[_total_measure_cost_incl_surtax_key])
        )

        return dict(_selected_measures_rows)

    def _get_quantity_cost_parameters(
        self,
        vc_parameters: dict[str, CostParameterProtocol],
        csv_dictionary: dict,
    ):
        def _format_parameter_name(dict_name: str) -> str:
            return dict_name.replace("_", " ").capitalize().strip()

        for (
            _parameter_name,
            _vc_parameter,
        ) in vc_parameters.items():
            _parameter_name = _format_parameter_name(_parameter_name)

            _quantity_key = f"{_parameter_name} {self._quantity_key_column}:"
            csv_dictionary[_quantity_key].append(
                round(_vc_parameter.quantity, self._decimals)
                if _vc_parameter
                else math.nan
            )

            _cost_key = f"{_parameter_name} {self._cost_key_column}:"
            csv_dictionary[_cost_key].append(
                round(_vc_parameter.total_cost, self._decimals)
                if _vc_parameter
                else math.nan
            )

            _cost_with_surtax_key = (
                f"{_parameter_name} {self._cost_with_surtax_key_column}:"
            )
            csv_dictionary[_cost_with_surtax_key].append(
                round(_vc_parameter.total_cost_with_surtax, self._decimals)
                if _vc_parameter
                else math.nan
            )
