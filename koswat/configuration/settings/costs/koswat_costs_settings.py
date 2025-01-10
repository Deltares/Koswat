import math
from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.costs.construction_costs_settings import (
    ConstructionCostsSettings,
)
from koswat.configuration.settings.costs.dike_profile_costs_settings import (
    DikeProfileCostsSettings,
)
from koswat.configuration.settings.costs.infastructure_costs_settings import (
    InfrastructureCostsSettings,
)
from koswat.configuration.settings.costs.surtax_costs_settings import (
    SurtaxCostsSettings,
)


@dataclass
class KoswatCostsSettings(KoswatConfigProtocol):
    price_year: int = math.nan
    dike_profile_costs: DikeProfileCostsSettings = None
    infrastructure_costs: InfrastructureCostsSettings = None
    surtax_costs: SurtaxCostsSettings = None
    construction_costs: ConstructionCostsSettings = None

    def is_valid(self) -> bool:
        return (
            not math.isnan(self.price_year)
            and self.dike_profile_costs.is_valid()
            and self.infrastructure_costs.is_valid()
            and self.surtax_costs.is_valid()
            and self.construction_costs.is_valid()
        )
