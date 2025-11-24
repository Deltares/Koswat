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
