"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
from koswat.cost_report.infrastructure.infrastructure_profile_costs_calculator import (
    InfrastructureProfileCostsCalculator,
)
from koswat.cost_report.infrastructure.multi_infrastructure_profile_costs_calculator import (
    MultiInfrastructureProfileCostsCalculator,
)
from koswat.dike.surroundings.road_class import RoadsClass
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass(kw_only=True)
class MultiInfrastructureProfileCostsCalculatorBuilder(BuilderProtocol):
    """
    Builder to set up "fix" information such as costs derived from the koswat
    settings (`InfraCostsEnum`, `SurtaxFactorEnum`) which directly determines the
    zone `A` and/or `B` costs that will be applied for each infrastructure.
    """

    reinforced_profile: ReinforcementProfileProtocol

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
        self, infrastructure_type: RoadsClass
    ) -> tuple[float, float]:
        if not self.cost_settings:
            return (math.nan, math.nan)
        if infrastructure_type == RoadsClass.CLASS_2:
            return (
                self.cost_settings.adding_roads_klasse2,
                self.cost_settings.removing_roads_klasse2,
            )
        if infrastructure_type == RoadsClass.CLASS_7:
            return (
                self.cost_settings.adding_roads_klasse7,
                self.cost_settings.removing_roads_klasse7,
            )
        if infrastructure_type == RoadsClass.CLASS_24:
            return (
                self.cost_settings.adding_roads_klasse24,
                self.cost_settings.removing_roads_klasse24,
            )
        if infrastructure_type == RoadsClass.CLASS_47:
            return (
                self.cost_settings.adding_roads_klasse47,
                self.cost_settings.removing_roads_klasse47,
            )
        if infrastructure_type == RoadsClass.CLASS_UNKNOWN:
            return (
                self.cost_settings.adding_roads_unknown,
                self.cost_settings.removing_roads_unknown,
            )
        return math.nan, math.nan

    def _get_zone_cost_for_non_rising_dike(
        self, adding_costs: float, removing_costs: float
    ) -> float:
        _0dh_factor = self.infrastructure_wrapper.non_rising_dike_costs_factor
        if _0dh_factor == InfraCostsEnum.GEEN:
            return 0
        elif _0dh_factor == InfraCostsEnum.HERSTEL:
            return adding_costs
        elif _0dh_factor == InfraCostsEnum.VERVANG:
            return adding_costs + removing_costs

        logging.error("`0dh` factor %s not supported.", _0dh_factor)
        return math.nan

    def _get_zone_a_costs(self, adding_costs: float, removing_costs: float) -> float:
        # Waterside zone costs
        if self.reinforced_profile.waterside_changed:
            return adding_costs + removing_costs
        return self._get_zone_cost_for_non_rising_dike(adding_costs, removing_costs)

    def _get_zone_b_costs(self, adding_costs: float, removing_costs: float) -> float:
        # Crest zone costs
        return self._get_zone_cost_for_non_rising_dike(adding_costs, removing_costs)

    def _get_zone_c_costs(self, adding_costs: float, removing_costs: float) -> float:
        # Polderside zone costs
        return adding_costs + removing_costs

    def _get_zone_costs(
        self, infrastructure_type: RoadsClass
    ) -> tuple[float, float, float]:
        _adding_costs, _removing_costs = self._get_infrastructure_costs(
            infrastructure_type
        )
        return (
            self._get_zone_a_costs(_adding_costs, _removing_costs),
            self._get_zone_b_costs(_adding_costs, _removing_costs),
            self._get_zone_c_costs(_adding_costs, _removing_costs),
        )

    def build(self) -> MultiInfrastructureProfileCostsCalculator:

        _surtax_costs = self._get_surtax_costs()

        def get_infra_calculator(
            infrastructure: SurroundingsInfrastructure,
        ) -> InfrastructureProfileCostsCalculator:
            _costs_a, _costs_b, _costs_c = self._get_zone_costs(
                infrastructure.infrastructure_type
            )
            return InfrastructureProfileCostsCalculator(
                infrastructure=infrastructure,
                surtax=_surtax_costs,
                zone_a_costs=_costs_a,
                zone_b_costs=_costs_b,
                zone_c_costs=_costs_c,
                buffer_crest_waterside=self.infrastructure_wrapper.buffer_crest_waterside,
            )

        return MultiInfrastructureProfileCostsCalculator(
            infrastructure_calculators=list(
                map(
                    get_infra_calculator,
                    self.infrastructure_wrapper.surroundings_collection.values(),
                )
            )
        )
