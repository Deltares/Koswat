import math
from collections.abc import Callable

import pytest

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
from koswat.dike.surroundings.infrastructure_types import RoadClassUnknown
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from tests.conftest import PointSurroundingsTestCase

_char_points = [(0.0, 0.0)] * 8


class TestMultiInfrastructureProfileCostsCalculatorBuilder:
    def test_initialize(self):
        # 1. Define test data.
        _builder = MultiInfrastructureProfileCostsCalculatorBuilder(
            reinforced_profile=None,
            infrastructure_wrapper=None,
            surtax_cost_settings=None,
        )

        # 2. Verify expectations
        assert isinstance(_builder, MultiInfrastructureProfileCostsCalculatorBuilder)
        assert isinstance(_builder, BuilderProtocol)
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
        "non_rising_dike_costs_factor",
        [
            pytest.param(_ice, id=f"Infra costs: {_ice.name.lower()}")
            for _ice in InfraCostsEnum
        ],
    )
    def test_build_given_different_settings(
        self,
        reinforcement_profile_builder: Callable[
            [list[tuple[float, float]], list[tuple[float, float]]],
            ReinforcementProfileProtocol,
        ],
        surtax_cost_factor: SurtaxFactorEnum,
        non_rising_dike_costs_factor: InfraCostsEnum,
        surroundings_infrastructure_fixture: tuple[
            SurroundingsInfrastructure, PointSurroundingsTestCase
        ],
    ):
        # 1. Define test data.
        _infrastructure, _ = surroundings_infrastructure_fixture
        # _infrastructure.infrastructure_type = RoadClassUnknown()
        _infra_wrapper = InfrastructureSurroundingsWrapper(
            infrastructures_considered=True,
            surtax_cost_factor=surtax_cost_factor,
            non_rising_dike_costs_factor=non_rising_dike_costs_factor,
            infrastructures_collection={
                _infrastructure.infrastructure_type.infrastructure_name: _infrastructure
            },
        )

        _reinforced_profile = reinforcement_profile_builder(_char_points, _char_points)
        _builder = MultiInfrastructureProfileCostsCalculatorBuilder(
            reinforced_profile=_reinforced_profile,
            infrastructure_wrapper=_infra_wrapper,
            surtax_cost_settings=SurtaxCostsSettings(
                roads_normal=1.0, roads_easy=0.5, roads_hard=2.0
            ),
        )

        _expected_surtax_cost = 1.0
        if surtax_cost_factor == SurtaxFactorEnum.MAKKELIJK:
            _expected_surtax_cost = 0.5
        if surtax_cost_factor == SurtaxFactorEnum.MOEILIJK:
            _expected_surtax_cost = 2.0

        _expected_zone_a_costs = 0.0
        _expected_zone_b_costs = 0.0
        _expected_zone_c_costs = (
            _infrastructure.infrastructure_type.adding_costs
            + _infrastructure.infrastructure_type.removing_costs
        )
        if non_rising_dike_costs_factor == InfraCostsEnum.HERSTEL:
            _expected_zone_a_costs = _infrastructure.infrastructure_type.adding_costs
            _expected_zone_b_costs = _infrastructure.infrastructure_type.adding_costs
        if non_rising_dike_costs_factor == InfraCostsEnum.VERVANG:
            _expected_zone_a_costs = (
                _infrastructure.infrastructure_type.adding_costs
                + _infrastructure.infrastructure_type.removing_costs
            )
            _expected_zone_b_costs = (
                _infrastructure.infrastructure_type.adding_costs
                + _infrastructure.infrastructure_type.removing_costs
            )

        # 2. Run test.
        _calculator = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_calculator, MultiInfrastructureProfileCostsCalculator)
        assert isinstance(_calculator.infrastructure_calculators, list)
        # One calculator for each of the property types.
        _expected_calculators = len(_infra_wrapper.infrastructures_collection)
        assert len(_calculator.infrastructure_calculators) == _expected_calculators

        def general_calculator_validation(
            infra_calculator: InfrastructureProfileCostsCalculator,
        ) -> bool:
            assert isinstance(infra_calculator, InfrastructureProfileCostsCalculator)
            assert infra_calculator.surtax == _expected_surtax_cost
            if (
                infra_calculator.infrastructure.infrastructure_type
                != _infrastructure.infrastructure_type
            ):
                if non_rising_dike_costs_factor == InfraCostsEnum.GEEN:
                    assert infra_calculator.zone_a_costs == 0.0
                    assert infra_calculator.zone_b_costs == 0.0
                else:
                    assert math.isnan(infra_calculator.zone_a_costs)
                    assert math.isnan(infra_calculator.zone_b_costs)
                assert math.isnan(infra_calculator.zone_c_costs)
            else:
                assert infra_calculator.zone_a_costs == _expected_zone_a_costs
                assert infra_calculator.zone_b_costs == _expected_zone_b_costs
                assert infra_calculator.zone_c_costs == _expected_zone_c_costs
            return True

        assert all(
            general_calculator_validation(_c)
            for _c in _calculator.infrastructure_calculators
        )

    @pytest.mark.parametrize(
        "waterside_changed, non_rising_dike_costs_factor, expected_zone_a_costs",
        [
            pytest.param(False, InfraCostsEnum.GEEN, 0.0, id="No change - GEEN"),
            pytest.param(False, InfraCostsEnum.HERSTEL, 24.0, id="No change - HERSTEL"),
            pytest.param(False, InfraCostsEnum.VERVANG, 36.0, id="No change - VERVANG"),
            pytest.param(True, InfraCostsEnum.GEEN, 36.0, id="Changed - GEEN"),
            pytest.param(True, InfraCostsEnum.HERSTEL, 36.0, id="Changed - HERSTEL"),
            pytest.param(True, InfraCostsEnum.VERVANG, 36.0, id="Changed - VERVANG"),
        ],
    )
    def test_build_given_different_reinforcement_profile(
        self,
        reinforcement_profile_builder: Callable[
            [list[tuple[float, float]], list[tuple[float, float]]],
            ReinforcementProfileProtocol,
        ],
        waterside_changed: bool,
        non_rising_dike_costs_factor: InfraCostsEnum | None,
        expected_zone_a_costs: float,
    ):
        # 1. Define test data.
        _infrastructure = SurroundingsInfrastructure(
            infrastructure_type=RoadClassUnknown(
                width=10.0,
                adding_costs=24.0,
                removing_costs=12.0,
            ),
            points=[],
        )
        _infra_wrapper = InfrastructureSurroundingsWrapper(
            infrastructures_considered=True,
            surtax_cost_factor=SurtaxFactorEnum.NORMAAL,
            non_rising_dike_costs_factor=non_rising_dike_costs_factor,
            infrastructures_collection={
                _infrastructure.infrastructure_type.infrastructure_name: _infrastructure
            },
        )
        _reinforced_profile = reinforcement_profile_builder(_char_points, _char_points)
        _reinforced_profile.waterside_changed = waterside_changed
        _builder = MultiInfrastructureProfileCostsCalculatorBuilder(
            reinforced_profile=_reinforced_profile,
            infrastructure_wrapper=_infra_wrapper,
            surtax_cost_settings=SurtaxCostsSettings(
                roads_normal=1.0, roads_easy=0.5, roads_hard=2.0
            ),
        )

        # 2. Run test.
        _calculator = _builder.build()

        # Verify expectations
        _infra_cost_calculator = next(
            (
                x
                for x in _calculator.infrastructure_calculators
                if isinstance(x.infrastructure.infrastructure_type, RoadClassUnknown)
            ),
            None,
        )
        assert _infra_cost_calculator is not None
        assert _infra_cost_calculator.zone_a_costs == expected_zone_a_costs
