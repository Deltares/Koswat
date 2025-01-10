import math

import pytest

from koswat.configuration.settings.costs.infastructure_costs_settings import (
    InfrastructureCostsSettings,
)
from koswat.configuration.settings.costs.surtax_costs_settings import (
    SurtaxCostsSettings,
)
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.infrastructure.infrastructure_profile_costs_calculator import (
    InfrastructureProfileCostsCalculator,
)
from koswat.cost_report.infrastructure.multi_infrastructure_profile_costs_calculator import (
    MultiInfrastructureProfileCostsCalculator,
)
from koswat.cost_report.infrastructure.multi_infrastructure_profile_costs_calculator_builder import (
    MultiInfrastructureProfileCostsCalculatorBuilder,
)
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)
from tests.conftest import PointSurroundingsTestCase


class TestMultiInfrastructureProfileCostsCalculatorBuilder:
    def test_initialize(self):
        # 1. Define test data.
        _builder = MultiInfrastructureProfileCostsCalculatorBuilder(
            cost_settings=None, infrastructure_wrapper=None, surtax_cost_settings=None
        )

        # 2. Verify expectations
        assert isinstance(_builder, MultiInfrastructureProfileCostsCalculatorBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.cost_settings
        assert not _builder.infrastructure_wrapper
        assert not _builder.surtax_cost_settings

    @pytest.mark.parametrize(
        "surtax_cost_factor",
        [
            pytest.param(_sf, id=f"Surtax Factor: {_sf.name.lower()}")
            for _sf in SurtaxFactorEnum
        ],
    )
    @pytest.mark.parametrize(
        "dh0_factor",
        [
            pytest.param(_ice, id=f"Infra costs: {_ice.name.lower()}")
            for _ice in InfraCostsEnum
        ],
    )
    def test_build_given_different_settings(
        self,
        surtax_cost_factor: SurtaxFactorEnum,
        dh0_factor: InfraCostsEnum,
        surroundings_infrastructure_fixture: tuple[
            SurroundingsInfrastructure, PointSurroundingsTestCase
        ],
    ):
        # 1. Define test data.
        _infrastructure, _ = surroundings_infrastructure_fixture
        _infra_wrapper = InfrastructureSurroundingsWrapper(
            infrastructures_considered=True,
            surtax_cost_factor=surtax_cost_factor,
            non_rising_dike_costs_factor=dh0_factor,
            roads_class_unknown_polderside=_infrastructure,
        )
        _infrastructure.infrastructure_name = "roads_class_unknown_polderside"

        _adding_roads = 24.0
        _removing_roads = 12.0

        _builder = MultiInfrastructureProfileCostsCalculatorBuilder(
            cost_settings=InfrastructureCostsSettings(
                adding_roads_unknown=_adding_roads,
                removing_roads_unknown=_removing_roads,
            ),
            infrastructure_wrapper=_infra_wrapper,
            surtax_cost_settings=SurtaxCostsSettings(
                roads_normal=1.0, roads_easy=0.5, roads_hard=2.0
            ),
        )

        _expected_surtax_cost = 1.0
        if surtax_cost_factor == SurtaxFactorEnum.MAKKELIJK:
            _expected_surtax_cost = 0.5
        if surtax_cost_factor == SurtaxFactorEnum.MOEILIJK:
            _expected_surtax_cost = 2

        _expected_zone_a_costs = 0
        _expected_zone_b_costs = _adding_roads + _removing_roads
        if dh0_factor == InfraCostsEnum.HERSTEL:
            _expected_zone_a_costs = _adding_roads
        if dh0_factor == InfraCostsEnum.VERVANG:
            _expected_zone_a_costs = _adding_roads + _removing_roads

        # 2. Run test.
        _calculator = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_calculator, MultiInfrastructureProfileCostsCalculator)
        assert isinstance(_calculator.infrastructure_calculators, list)
        # One calculator for each of the property types.
        _expected_calculators = len(_infra_wrapper.surroundings_collection)
        assert len(_calculator.infrastructure_calculators) == _expected_calculators

        def general_calculator_validation(
            infra_calculator: InfrastructureProfileCostsCalculator,
        ) -> bool:
            assert isinstance(infra_calculator, InfrastructureProfileCostsCalculator)
            assert infra_calculator.surtax == _expected_surtax_cost
            if (
                infra_calculator.infrastructure.infrastructure_name
                != _infrastructure.infrastructure_name
            ):
                if dh0_factor == InfraCostsEnum.GEEN:
                    assert infra_calculator.zone_a_costs == 0
                else:
                    assert math.isnan(infra_calculator.zone_a_costs)
                assert math.isnan(infra_calculator.zone_b_costs)
            else:
                assert infra_calculator.zone_a_costs == _expected_zone_a_costs
                assert infra_calculator.zone_b_costs == _expected_zone_b_costs
            return True

        assert all(
            general_calculator_validation(_c)
            for _c in _calculator.infrastructure_calculators
        )
