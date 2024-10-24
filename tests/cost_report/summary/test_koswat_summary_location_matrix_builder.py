from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.summary.koswat_summary_location_matrix_builder import (
    KoswatSummaryLocationMatrixBuilder,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class TestKoswatSummaryLocationMatrixBuilder:
    def test_initialize(self):
        # Test just to verify design principle of parameterless
        # constructors is met.
        _builder = KoswatSummaryLocationMatrixBuilder()
        assert isinstance(_builder, KoswatSummaryLocationMatrixBuilder)
        assert isinstance(_builder, BuilderProtocol)

    def test_given_no_profile_report_list_then_returns_expected_matrix(self):
        # 1. Define test data.
        _builder = KoswatSummaryLocationMatrixBuilder()
        _section = "A"

        _builder.available_locations = [
            PointSurroundings(section=_section, traject_order=1),
            PointSurroundings(section=_section, traject_order=2),
        ]
        _builder.locations_profile_report_list = []

        # 2. Run test.
        _strategy_locations = _builder.build()

        # 3. Verify final expectations.
        assert isinstance(_strategy_locations, list)
        assert len(_strategy_locations) == len(_builder.available_locations)
        for _sl in _strategy_locations:
            assert _sl.point_surrounding in _builder.available_locations
            assert _sl.strategy_reinforcement_type_costs == []

    def test_given_profile_report_list_then_returns_expected_matrix(self):
        class MyMockedReinforcementProfile(ReinforcementProfileProtocol):
            output_name: str = "MockedReinforcementProfile"
            new_ground_level_surface: float = 42.0

        # 1. Define test data.
        _section = "A"
        _locations = [
            PointSurroundings(section=_section, traject_order=1),
            PointSurroundings(section=_section, traject_order=2),
        ]

        _profile_report = MultiLocationProfileCostReport()
        _profile_report.report_locations = _locations[:1]
        _profile_report.profile_cost_report = ProfileCostReport()
        _profile_report.profile_cost_report.reinforced_profile = (
            MyMockedReinforcementProfile()
        )

        _builder = KoswatSummaryLocationMatrixBuilder()
        _builder.available_locations = _locations
        _builder.locations_profile_report_list = [_profile_report]

        # 2. Run test.
        _strategy_locations = _builder.build()

        # 3. Verify final expectations.
        assert isinstance(_strategy_locations, list)
        assert len(_strategy_locations) == len(_builder.available_locations)
        assert _strategy_locations[0].point_surrounding in _builder.available_locations
        assert len(_strategy_locations[0].strategy_reinforcement_type_costs) == 1
        assert (
            _strategy_locations[0]
            .strategy_reinforcement_type_costs[0]
            .reinforcement_type
            == MyMockedReinforcementProfile
        )
        for _sl in _strategy_locations[1:]:
            assert _sl.point_surrounding in _builder.available_locations
            assert _sl.strategy_reinforcement_type_costs == []
