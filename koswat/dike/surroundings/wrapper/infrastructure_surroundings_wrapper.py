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

from dataclasses import dataclass, field

from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from koswat.dike.surroundings.surroundings_enum import SurroundingsEnum
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.wrapper.base_surroundings_wrapper import (
    BaseSurroundingsWrapper,
)


@dataclass
class InfrastructureSurroundingsWrapper(BaseSurroundingsWrapper):

    infrastructures_considered: bool = True

    # opslagfactor_wegen
    surtax_cost_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL

    # infrakosten_0dh
    non_rising_dike_costs_factor: InfraCostsEnum = InfraCostsEnum.GEEN

    # Polderside infrastructures
    roads_class_2_polderside: SurroundingsInfrastructure = field(
        default_factory=lambda: SurroundingsInfrastructure(
            infrastructure_name=SurroundingsEnum.ROADS_CLASS_2_POLDERSIDE.name
        )
    )
    roads_class_7_polderside: SurroundingsInfrastructure = field(
        default_factory=lambda: SurroundingsInfrastructure(
            infrastructure_name=SurroundingsEnum.ROADS_CLASS_7_POLDERSIDE.name
        )
    )
    roads_class_24_polderside: SurroundingsInfrastructure = field(
        default_factory=lambda: SurroundingsInfrastructure(
            infrastructure_name=SurroundingsEnum.ROADS_CLASS_24_POLDERSIDE.name
        )
    )
    roads_class_47_polderside: SurroundingsInfrastructure = field(
        default_factory=lambda: SurroundingsInfrastructure(
            infrastructure_name=SurroundingsEnum.ROADS_CLASS_47_POLDERSIDE.name
        )
    )
    roads_class_unknown_polderside: SurroundingsInfrastructure = field(
        default_factory=lambda: SurroundingsInfrastructure(
            infrastructure_name=SurroundingsEnum.ROADS_CLASS_UNKNOWN_POLDERSIDE.name
        )
    )

    # Waterside infrastructures (not supported yet)
    roads_class_2_waterside: SurroundingsInfrastructure = None
    roads_class_7_waterside: SurroundingsInfrastructure = None
    roads_class_24_waterside: SurroundingsInfrastructure = None
    roads_class_47_waterside: SurroundingsInfrastructure = None
    roads_class_unknown_waterside: SurroundingsInfrastructure = None
