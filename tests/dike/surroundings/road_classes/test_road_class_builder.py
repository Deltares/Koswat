import pytest

from koswat.configuration.io.config_sections.infrastructure_section_fom import (
    InfrastructureSectionFom,
)
from koswat.configuration.settings.costs.infastructure_costs_settings import (
    InfrastructureCostsSettings,
)
from koswat.dike.surroundings.road_classes import (
    RoadClassBuilder,
    RoadClassProtocol,
)


class TestRoadClassBuilder:

    def test_when_initialized_then_builder_created(self):
        # 1. Define test data
        _infrastructure_section_fom = None
        _infrastructure_costs_settings = None

        # 2. Execute test
        _builder = RoadClassBuilder(
            infrastructure_section=_infrastructure_section_fom,
            infrastructure_costs=_infrastructure_costs_settings,
        )

        # 3. Verify test results
        assert _builder is not None
        assert _builder.road_class_types is not None
        assert isinstance(_builder.road_class_types, list)
        assert all(
            isinstance(item, RoadClassProtocol) for item in _builder.road_class_types
        )

    @pytest.mark.parametrize(
        "name, expected_type, is_polderside",
        [
            pytest.param(x.polderside_name, x, True, id=x.polderside_name)
            for x in RoadClassBuilder(None, None).road_class_types
        ]
        + [
            pytest.param(x.waterside_name, x, False, id=x.waterside_name)
            for x in RoadClassBuilder(None, None).road_class_types
        ],
    )
    def test_when_build_given_valid_parameters_then_road_classes_created(
        self,
        infrastructure_section_fom_fixture: InfrastructureSectionFom,
        infrastructure_costs_settings_fixture: InfrastructureCostsSettings,
        name: str,
        expected_type: type[RoadClassProtocol],
        is_polderside: bool,
    ):
        # Define test data
        _builder = RoadClassBuilder(
            infrastructure_section=infrastructure_section_fom_fixture,
            infrastructure_costs=infrastructure_costs_settings_fixture,
        )

        # 2. Execute test
        _result = _builder.build(name)

        # 3. Verify expectations
        assert _result is not None
        assert isinstance(_result, RoadClassProtocol)
        assert isinstance(_result, expected_type)
        assert _result.is_polderside is is_polderside

    def test_when_build_given_invalid_parameters_then_none_returned(
        self,
        infrastructure_section_fom_fixture: InfrastructureSectionFom,
        infrastructure_costs_settings_fixture: InfrastructureCostsSettings,
    ):
        # 1. Define test data
        _builder = RoadClassBuilder(
            infrastructure_section=infrastructure_section_fom_fixture,
            infrastructure_costs=infrastructure_costs_settings_fixture,
        )

        # 2. Execute test
        _result = _builder.build("invalid")

        # 3. Verify expectations
        assert _result is None
