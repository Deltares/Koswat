from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


class UnitPrices(KoswatConfigProtocol):
    prijspeil: float


class DikeProfilesCosts(KoswatConfigProtocol):
    aanleg_graslaag_m3: float
    aanleg_kleilaag_m3: float
    aanleg_kern_m3: float
    hergebruik_graslaag_m3: float
    hergebruik_kern_m3: float
    afvoeren_materiaal_m3: float
    profileren_graslaag_m2: float
    profileren_kleilaag_m2: float
    profileren_kern_m2: float
    bewerken_maaiveld_m2: float


class InfrastructureCosts(KoswatConfigProtocol):
    wegen_klasse2_verwijderen: float
    wegen_klasse24_verwijderen: float
    wegen_klasse47_verwijderen: float
    wegen_klasse7_verwijderen: float
    wegen_onbekend_verwijderen: float
    wegen_klasse2_aanleg: float
    wegen_klasse24_aanleg: float
    wegen_klasse47_aanleg: float
    wegen_klasse7_aanleg: float
    wegen_onbekend_aanleg: float


class StoringCostsIncludingTaxes(KoswatConfigProtocol):
    grond_makkelijk: float
    grond_normaal: float
    grond_moeilijk: float
    constructief_makkelijk: float
    constructief_normaal: float
    constructief_moeilijk: float
    wegen_makkelijk: float
    wegen_normaal: float
    wegen_moeilijk: float
    grondaankoop_makkelijk: float
    grondaankoop_normaal: float
    grondaankoop_moeilijk: float


class StoringCostsExcludingTaxes(KoswatConfigProtocol):
    grond_makkelijk: float
    grond_normaal: float
    grond_moeilijk: float
    constructief_makkelijk: float
    constructief_normaal: float
    constructief_moeilijk: float
    wegen_makkelijk: float
    wegen_normaal: float
    wegen_moeilijk: float
    grondaankoop_makkelijk: float
    grondaankoop_normaal: float
    grondaankoop_moeilijk: float


class KoswatCosts(KoswatConfigProtocol):
    eenheidsprijzen_section: UnitPrices
    kostendijkprofiel_section: DikeProfilesCosts
    kosteninfrastructuur_section: InfrastructureCosts
    kostenopslagfactoreninclbtw_section: StoringCostsIncludingTaxes
    kostenopslagfactorenexclbtw_section: StoringCostsExcludingTaxes

    def __init__(self) -> None:
        self.eenheidsprijzen_section = None
        self.kostendijkprofiel_section = None
        self.kosteninfrastructuur_section = None
        self.kostenopslagfactoreninclbtw_section = None
        self.kostenopslagfactorenexclbtw_section = None

    def is_valid(self) -> bool:
        def valid_prop_config(config_property: KoswatConfigProtocol) -> bool:
            return config_property is not None and config_property.is_valid()

        return all(valid_prop_config(_config) for _config in dict(self).values())
