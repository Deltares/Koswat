from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from koswat.core.io.csv.koswat_csv_multi_header_fom import KoswatCsvMultiHeaderFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.infrastructure.infrastructure_location_costs import (
    InfrastructureLocationCosts,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class SummaryInfrastructureCostsCsvFomBuilder(BuilderProtocol):
    koswat_summary: KoswatSummary
    _ordered_profile_types: list[str] = field(default_factory=list)
    _ordered_infra_types: list[str] = field(default_factory=list)

    def build(self) -> KoswatCsvMultiHeaderFom:
        self._ordered_profile_types = list(
            map(
                lambda x: x.profile_type_name,
                self.koswat_summary.locations_profile_report_list,
            )
        )
        self._ordered_infra_types = sorted(
            list(
                set(
                    _ilpcr.infrastructure_name
                    for _ilpcr in self.koswat_summary.locations_profile_report_list[
                        0
                    ].infra_multilocation_profile_cost_report
                )
            )
        )

        return KoswatCsvMultiHeaderFom(
            headers=self._get_headers(),
            entries=self._get_locations_matrix(
                self.koswat_summary.reinforcement_per_locations,
                self.koswat_summary.locations_profile_report_list,
            ),
        )

    def _get_locations_matrix(
        self,
        reinforcement_per_locations: list[StrategyLocationReinforcement],
        locations_profile_report_list: list[MultiLocationProfileCostReport],
    ) -> list[list[Any]]:
        def _get_totals(location: PointSurroundings) -> list[float]:
            return list(
                round(
                    sum(
                        _ilc.total_cost_with_surtax
                        for _ilc in _infra_cost_per_loc_dict[location][
                            _profile_type
                        ].values()
                    ),
                    2,
                )
                for _profile_type in self._ordered_profile_types
            )

        def _get_details(location: PointSurroundings, profile_type: str) -> list[float]:
            _details = []
            for _infra_type in self._ordered_infra_types:
                _ilc = _infra_cost_per_loc_dict[location][profile_type][_infra_type]
                _details.extend(
                    [
                        _ilc.zone_a,
                        round(_ilc.zone_a_costs * _ilc.surtax, 2),
                        _ilc.zone_b,
                        round(_ilc.zone_b_costs * _ilc.surtax, 2),
                    ]
                )
            return _details

        def _location_as_row(
            matrix_item: tuple[PointSurroundings, list[int]]
        ) -> list[Any]:
            _ps, _m_values = matrix_item
            _location_as_row = [_ps.section, _ps.location.x, _ps.location.y]
            _location_as_row.extend(_m_values)
            return _location_as_row

        _infra_cost_per_loc_dict = self._get_infra_location_costs(
            locations_profile_report_list
        )

        # Initiate locations matrix
        _matrix = defaultdict(list)

        # Totals and details per location for profile types
        for _rpl in reinforcement_per_locations:
            _totals = _get_totals(_rpl.location)
            _details = []
            for _profile_type in self._ordered_profile_types:
                _details.extend(_get_details(_rpl.location, _profile_type))
            _matrix[_rpl.location] = _totals + _details

        return list(
            map(
                _location_as_row,
                sorted(_matrix.items(), key=lambda x: x[0].traject_order),
            )
        )

    def _get_infra_location_costs(
        self,
        locations_profile_report_list: list[MultiLocationProfileCostReport],
    ) -> dict[PointSurroundings, dict[str, dict[str, InfrastructureLocationCosts]]]:
        """
        Create a dictionary with the infrastructure cost per location/profile type/infra type.

        Args:
            locations_profile_report_list (list[MultiLocationProfileCostReport]):
                List containing all the chosen profiles with their costs.

        Returns:
            dict[ PointSurroundings, dict[str, dict[str, InfrastructureLocationCosts]] ]:
                Dict containing the infrastructure cost per location/profile type/infra type.
        """
        _infra_location_cost_dict: dict[
            PointSurroundings,
            dict[str, dict[str, InfrastructureLocationCosts]],
        ] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(InfrastructureLocationCosts))
        )

        def update_infra_location_cost_dict(
            location: PointSurroundings,
            profile_type_name: str,
            infra_name: str,
            costs: InfrastructureLocationCosts,
        ):
            _infra_location_cost_dict[location][profile_type_name][infra_name] = costs

        for _lpr in locations_profile_report_list:
            for _ilpcr in _lpr.infra_multilocation_profile_cost_report:
                update_infra_location_cost_dict(
                    _ilpcr.infrastructure_location_costs.location,
                    _lpr.profile_type_name,
                    _ilpcr.infrastructure_name,
                    _ilpcr.infrastructure_location_costs,
                )

        return _infra_location_cost_dict

    def _get_headers(self) -> list[list[str]]:
        """
        Get the headers for the CSV file.
            Line 1: Profile types
            Line 2: Infra types
            Line 3: Zone A and B lengths and costs

        Returns:
            list[list[str]]: Headers for the CSV file.
        """
        _headers = []
        _zone_key = "Zone"
        _length_key = "Lengte (m)"
        _cost_key = "Kosten* (Euro)"
        _total_cost_key = "Totale kosten* (Euro)"
        _surtax_note = "*) Kosten incl. opslagfactoren"

        # Collect header fragments
        _zones = ["A", "B"]
        _zone_keys = []
        for _zone in _zones:
            _zone_keys.extend(
                [
                    f"{_zone_key} {_zone} {_length_key}",
                    f"{_zone_key} {_zone} {_cost_key}",
                ]
            )

        _infra_type_keys = []
        for _infra_type in self._ordered_infra_types:
            _infra_type_keys.append(_infra_type)
            _infra_type_keys.extend([""] * (len(_zone_keys) - 1))

        # Build headers (first 3 columns for the location)
        _headers = [
            ["", "", ""],
            ["", "", ""],
            ["Section", "X coord", "Y coord"],
        ]

        # Total cost headers per profile type
        _headers[0].extend(self._ordered_profile_types)
        _headers[1].extend(
            [_surtax_note] + [""] * (len(self._ordered_profile_types) - 1)
        )
        _headers[2].extend([_total_cost_key] * len(self._ordered_profile_types))

        # Cost detail headers per profile type, infra type and zone
        for _profile_type in self._ordered_profile_types:
            _headers[0].append(_profile_type)
            _headers[0].extend(
                [""] * (len(self._ordered_infra_types) * len(_zone_keys) - 1)
            )
            _headers[1].extend(_infra_type_keys)
            for _infra_type in self._ordered_infra_types:
                _headers[2].extend(_zone_keys)

        return _headers
