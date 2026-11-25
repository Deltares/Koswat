import pytest

from koswat.configuration.io.config_sections.infrastructure_section_fom import (
    InfrastructureSectionFom,
)
from koswat.configuration.settings.costs.infastructure_costs_settings import (
    InfrastructureCostsSettings,
)
from koswat.dike.surroundings.infrastructure_types import (
    InfrastructureTypeBuilder,
    InfrastructureTypeProtocol,
)


class TestInfrastructureTypeBuilder:

    def test_when_initialized_then_builder_created(self):
        # 1. Define test data
        _infrastructure_section_fom = None
        _infrastructure_costs_settings = None

        # 2. Execute test
        _builder = InfrastructureTypeBuilder(
            infrastructure_section=_infrastructure_section_fom,
            infrastructure_costs=_infrastructure_costs_settings,
        )

        # 3. Verify test results
        assert _builder is not None
        assert _builder.infrastructure_types is not None

    @pytest.mark.parametrize(
        "source_name, expected_type, is_polderside",
        [
            pytest.param(
                x.get_polderside_import_name(),
                x,
                True,
                id=x.get_polderside_import_name(),
            )
            for x in InfrastructureTypeBuilder(None, None).infrastructure_types
        ]
        + [
            pytest.param(
                x.get_waterside_import_name(),
                x,
                False,
                id=x.get_waterside_import_name(),
            )
            for x in InfrastructureTypeBuilder(None, None).infrastructure_types
        ],
    )
    def test_when_build_given_valid_parameters_then_infrastructure_type_created(
        self,
        infrastructure_section_fom_fixture: InfrastructureSectionFom,
        infrastructure_costs_settings_fixture: InfrastructureCostsSettings,
        source_name: str,
        expected_type: type[InfrastructureTypeProtocol],
        is_polderside: bool,
    ):
        # Define test data
        _builder = InfrastructureTypeBuilder(
            infrastructure_section=infrastructure_section_fom_fixture,
            infrastructure_costs=infrastructure_costs_settings_fixture,
        )

        # 2. Execute test
        _result = _builder.build(source_name)

        # 3. Verify expectations
        assert _result is not None
        assert isinstance(_result, InfrastructureTypeProtocol)
        assert isinstance(_result, expected_type)
        assert _result.is_polderside is is_polderside

    def test_when_build_given_invalid_parameters_then_none_returned(
        self,
        infrastructure_section_fom_fixture: InfrastructureSectionFom,
        infrastructure_costs_settings_fixture: InfrastructureCostsSettings,
    ):
        # 1. Define test data
        _builder = InfrastructureTypeBuilder(
            infrastructure_section=infrastructure_section_fom_fixture,
            infrastructure_costs=infrastructure_costs_settings_fixture,
        )

        # 2. Execute test
        _result = _builder.build("invalid")

        # 3. Verify expectations
        assert _result is None
