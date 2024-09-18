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
        _infrastructure, _test_case_data = surroundings_infrastructure_fixture
        _infra_wrapper = InfrastructureSurroundingsWrapper(
            infrastructures_considered=True,
            surtax_cost_factor=surtax_cost_factor,
            non_rising_dike_costs_factor=dh0_factor,
            roads_class_unknown_polderside=_infrastructure,
        )

        _builder = MultiInfrastructureProfileCostsCalculatorBuilder(
            cost_settings=InfrastructureCostsSettings(
                adding_roads_unknown=24.0, removing_roads_unknown=12.0
            ),
            infrastructure_wrapper=_infra_wrapper,
            surtax_cost_settings=SurtaxCostsSettings(
                roads_normal=1.0, roads_easy=0.5, roads_hard=2.0
            ),
        )

        # 2. Run test.
        _calculator = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_calculator, MultiInfrastructureProfileCostsCalculator)
        assert any(_calculator.infrastructure_calculators)
        assert all(
            isinstance(_c, InfrastructureProfileCostsCalculator)
            for _c in _calculator.infrastructure_calculators
        )
