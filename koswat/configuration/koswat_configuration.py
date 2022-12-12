from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.models.koswat_general_settings import *


class KoswatConfiguration(KoswatConfigProtocol):
    analysis_settings: AnalysisSettings
    dike_profile_settings: DikeProfileSettings
    soil_settings: SoilSettings
    pipingwall_settings: PipingwallSettings
    stabilitywall_settings: StabilitywallSettings
    cofferdam_settings: CofferdamSettings
    surroundings_settings: SurroundingsSettings
    infrastructure_settings: InfrastructuurSettings

    def __init__(self) -> None:
        self.analysis_settings = None
        self.dike_profile_settings = None
        self.soil_settings = None
        self.pipingwall_settings = None
        self.stabilitywall_settings = None
        self.cofferdam_settings = None
        self.surroundings_settings = None
        self.infrastructure_settings = None

    def is_valid(self) -> bool:
        def valid_prop_config(config_property: KoswatConfigProtocol) -> bool:
            return config_property is not None and config_property.is_valid()

        return all(valid_prop_config(_config) for _config in self.__dict__.values())
