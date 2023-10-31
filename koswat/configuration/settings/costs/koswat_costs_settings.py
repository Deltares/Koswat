import math

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


class KoswatCostsSettings(KoswatConfigProtocol):
    price_year: int
    dike_profile_costs: DikeProfileCostsSettings
    infrastructure_costs: InfrastructureCostsSettings
    surtax_costs: SurtaxCostsSettings
    construction_costs: ConstructionCostsSettings

    def __init__(self) -> None:
        self.price_year = math.nan
        self.dike_profile_costs = None
        self.infrastructure_costs = None
        self.surtax_costs = None
        self.construction_costs = ConstructionCostsSettings()

    def is_valid(self) -> bool:
        return (
            not math.isnan(self.price_year)
            and self.dike_profile_costs.is_valid()
            and self.infrastructure_costs.is_valid()
            and self.surtax_costs.is_valid()
            and self.construction_costs.is_valid()
        )
