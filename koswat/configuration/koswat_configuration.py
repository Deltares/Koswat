from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.models.koswat_general_settings import *


class KoswatConfiguration(KoswatConfigProtocol):
    analysis_settings: AnalysisSettings
    dike_profile_settings: DikeProfileSettings
    soil_settings: GrondmaatregelSettings
    piping_wall_settings: KwelschermSettings
    stability_wall_settings: StabiliteitswandSettings
    cofferdam_settings: KistdamSettings
    surroundings_settings: OmgevingSettings
    infrastructure_settings: InfrastructuurSettings

    def __init__(self) -> None:
        self.analysis_settings = None
        self.dike_profile_settings = None
        self.soil_settings = None
        self.piping_wall_settings = None
        self.stability_wall_settings = None
        self.cofferdam_settings = None
        self.surroundings_settings = None
        self.infrastructure_settings = None

    def is_valid(self) -> bool:
        def valid_prop_config(config_property: KoswatConfigProtocol) -> bool:
            return config_property is not None and config_property.is_valid()

        return all(valid_prop_config(_config) for _config in self.__dict__.values())
