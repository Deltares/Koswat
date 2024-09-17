import logging
import math
from dataclasses import dataclass

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
from koswat.cost_report.infrastructure.infrastructure_costs_calculator import (
    InfrastructureProfileCostsCalculator,
)
from koswat.cost_report.infrastructure.multi_infrastructure_profile_costs_calculator import (
    MultiInfrastructureProfileCostsCalculator,
)
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)


@dataclass
class MultiInfrastructureProfileCostsCalculatorBuilder(BuilderProtocol):

    infrastructure_wrapper: InfrastructureSurroundingsWrapper
    cost_settings: InfrastructureCostsSettings

    # We are only interested in the `roads_` properties.
    surtax_cost_settings: SurtaxCostsSettings

    def _get_surtax_costs(self) -> float:
        if not self.surtax_cost_settings:
            return math.nan

        if self.infrastructure_wrapper.surtax_cost_factor == SurtaxFactorEnum.NORMAAL:
            return self.surtax_cost_settings.roads_normal

        if self.infrastructure_wrapper.surtax_cost_factor == SurtaxFactorEnum.MOEILIJK:
            return self.surtax_cost_settings.roads_hard

        return self.surtax_cost_settings.roads_easy

    def _get_infrastructure_costs(
        self, infrastructure_name: str
    ) -> tuple[float, float]:
        if not self.cost_settings:
            return (math.nan, math.nan)
        if "_class_2_" in infrastructure_name:
            return (
                self.cost_settings.adding_roads_klasse2,
                self.cost_settings.removing_roads_klasse2,
            )
        if "_class_7_" in infrastructure_name:
            return (
                self.cost_settings.adding_roads_klasse7,
                self.cost_settings.removing_roads_klasse7,
            )
        if "_class_24_" in infrastructure_name:
            return (
                self.cost_settings.adding_roads_klasse24,
                self.cost_settings.removing_roads_klasse24,
            )
        if "_class_47_" in infrastructure_name:
            return (
                self.cost_settings.adding_roads_klasse47,
                self.cost_settings.removing_roads_klasse47,
            )
        if "_class_unknown_" in infrastructure_name:
            return (
                self.cost_settings.adding_roads_unknown,
                self.cost_settings.removing_roads_unknown,
            )
        return math.nan, math.nan

    def _get_zone_a_costs(self, adding_costs: float, removing_costs: float) -> float:
        _dh0_factor = self.infrastructure_wrapper.non_rising_dike_costs_factor
        if _dh0_factor == InfraCostsEnum.GEEN:
            return 0
        elif _dh0_factor == InfraCostsEnum.HERSTEL:
            return adding_costs
        elif _dh0_factor == InfraCostsEnum.VERVANG:
            return adding_costs + removing_costs

        logging.error("`dh0` factor %s not supported.", _dh0_factor)
        return math.nan

    def _get_zone_b_costs(self, adding_costs: float, removing_costs: float) -> float:
        return adding_costs + removing_costs

    def _get_zone_a_b_costs(self, infrastructure_name: str) -> tuple[float, float]:
        _adding_costs, _removing_costs = self._get_infrastructure_costs(
            infrastructure_name
        )
        return (
            self._get_zone_a_costs(_adding_costs, _removing_costs),
            self._get_zone_b_costs(_adding_costs, _removing_costs),
        )

    def build(self) -> MultiInfrastructureProfileCostsCalculator:

        _surtax_costs = self._get_surtax_costs()

        def get_infra_calculator(
            infrastructure_tuple: tuple[str, MultiInfrastructureProfileCostsCalculator]
        ) -> MultiInfrastructureProfileCostsCalculator:
            _costs_a, _costs_b = self._get_zone_a_b_costs(infrastructure_tuple[0])
            return InfrastructureProfileCostsCalculator(
                infrastructure=infrastructure_tuple[1],
                surtax_costs=_surtax_costs,
                zone_a_costs=_costs_a,
                zone_b_costs=_costs_b,
            )

        _calculators = {
            _infra[0]: get_infra_calculator(_infra)
            for _infra in self.infrastructure_wrapper.surroundings_collection.items()
        }

        return MultiInfrastructureProfileCostsCalculator(
            infrastructure_calculators=_calculators
        )
