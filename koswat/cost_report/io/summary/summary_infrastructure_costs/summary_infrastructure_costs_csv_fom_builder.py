from koswat.core.io.csv.koswat_csv_multi_header_fom import KoswatCsvMultiHeaderFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class SummaryInfrastructureCostsCsvFomBuilder(BuilderProtocol):
    koswat_summary: KoswatSummary

    def __init__(self) -> None:
        self.koswat_summary = None

    def build(self) -> KoswatCsvMultiHeaderFom:
        _csv_fom = KoswatCsvMultiHeaderFom()
        _csv_fom.headers = self._get_headers()
        _csv_fom.entries.append([0] * len(_csv_fom.headers[0]))  # TODO: get entries

        return _csv_fom

    def _get_headers(self) -> list[list[str]]:
        _headers = []
        _zone_key = "Zone"
        _length_key = "Lengte (m)"
        _cost_key = "Kosten (€)"
        _total_cost_key = "Totale kosten (€)"

        # Collect header fragments
        _ordered_profile_types = list(
            map(
                lambda x: x.profile_type_name,
                self.koswat_summary.locations_profile_report_list,
            )
        )

        _zones = ["A", "B"]
        _zone_keys = []
        for _zone in _zones:
            _zone_keys.extend(
                [
                    f"{_zone_key} {_zone} {_length_key}",
                    f"{_zone_key} {_zone} {_cost_key}",
                ]
            )

        _road_types = [
            "Road Klasse2",
            "Road Klasse24",
        ]  # TODO: get road types from koswat_summary
        _road_type_keys = []
        for _road_type in _road_types:
            _road_type_keys.append(_road_type)
            _road_type_keys.extend([""] * (len(_zone_keys) - 1))

        # Build headers
        _headers = [
            ["", "", ""],
            ["", "", ""],
            ["Section", "X coord", "Y coord"],
        ]

        # Total cost per profile type
        _headers[0].extend(_ordered_profile_types)
        _headers[1].extend([""] * len(_ordered_profile_types))
        _headers[2].extend([_total_cost_key] * len(_ordered_profile_types))

        # Profile details per road type and zone
        for _profile_type in _ordered_profile_types:
            _headers[0].append(_profile_type)
            _headers[0].extend([""] * (len(_road_types) * len(_zone_keys) - 1))
            _headers[1].extend(_road_type_keys)
            for _road_type in _road_types:
                _headers[2].extend(_zone_keys)

        return _headers
