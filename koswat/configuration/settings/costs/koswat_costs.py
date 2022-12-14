import math

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.costs.dike_profile_costs_settings import (
    DikeProfileCostsSettings,
)
from koswat.configuration.settings.costs.infastructure_costs_settings import (
    InfrastructureCostsSettings,
)
from koswat.configuration.settings.costs.storage_costs_settings import (
    StorageCostsSettings,
)


class KoswatCostsSettings(KoswatConfigProtocol):
    price_year: int  # Should be an int.
    dike_profile_costs: DikeProfileCostsSettings
    infrastructure_costs: InfrastructureCostsSettings
    storage_costs: StorageCostsSettings

    def __init__(self) -> None:
        self.price_year = math.nan
        self.dike_profile_costs = None
        self.infrastructure_costs = None
        self.storage_costs = None

    def is_valid(self) -> bool:
        return (
            not math.isnan(self.price_year)
            and self.dike_profile_costs.is_valid()
            and self.infrastructure_costs.is_valid()
            and self.storage_costs.is_valid()
        )
