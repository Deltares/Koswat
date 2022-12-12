import math

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)


class UnitPrices(KoswatConfigProtocol):
    prijspeil: float

    def __init__(self) -> None:
        self.prijspeil = math.nan

    def is_valid(self) -> bool:
        return not math.isnan(self.prijspeil)


class DikeProfileCosts(KoswatConfigProtocol):
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

    def __init__(self) -> None:
        self.aanleg_graslaag_m3 = math.nan
        self.aanleg_kleilaag_m3 = math.nan
        self.aanleg_kern_m3 = math.nan
        self.hergebruik_graslaag_m3 = math.nan
        self.hergebruik_kern_m3 = math.nan
        self.afvoeren_materiaal_m3 = math.nan
        self.profileren_graslaag_m2 = math.nan
        self.profileren_kleilaag_m2 = math.nan
        self.profileren_kern_m2 = math.nan
        self.bewerken_maaiveld_m2 = math.nan

    def is_valid(self) -> bool:
        return all(
            _valid_float_prop(_prop) for _prop in super(DikeProfileCosts, self).values()
        )


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

    def __init__(self) -> None:
        self.wegen_klasse2_verwijderen = math.nan
        self.wegen_klasse24_verwijderen = math.nan
        self.wegen_klasse47_verwijderen = math.nan
        self.wegen_klasse7_verwijderen = math.nan
        self.wegen_onbekend_verwijderen = math.nan
        self.wegen_klasse2_aanleg = math.nan
        self.wegen_klasse24_aanleg = math.nan
        self.wegen_klasse47_aanleg = math.nan
        self.wegen_klasse7_aanleg = math.nan
        self.wegen_onbekend_aanleg = math.nan

    def is_valid(self) -> bool:
        return all(
            _valid_float_prop(_prop)
            for _prop in super(InfrastructureCosts, self).values()
        )


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

    def __init__(self) -> None:
        self.grond_makkelijk = math.nan
        self.grond_normaal = math.nan
        self.grond_moeilijk = math.nan
        self.constructief_makkelijk = math.nan
        self.constructief_normaal = math.nan
        self.constructief_moeilijk = math.nan
        self.wegen_makkelijk = math.nan
        self.wegen_normaal = math.nan
        self.wegen_moeilijk = math.nan
        self.grondaankoop_makkelijk = math.nan
        self.grondaankoop_normaal = math.nan
        self.grondaankoop_moeilijk = math.nan

    def is_valid(self) -> bool:
        return all(
            _valid_float_prop(_prop)
            for _prop in super(StoringCostsIncludingTaxes, self).values()
        )


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

    def __init__(self) -> None:
        self.grond_makkelijk = math.nan
        self.grond_normaal = math.nan
        self.grond_moeilijk = math.nan
        self.constructief_makkelijk = math.nan
        self.constructief_normaal = math.nan
        self.constructief_moeilijk = math.nan
        self.wegen_makkelijk = math.nan
        self.wegen_normaal = math.nan
        self.wegen_moeilijk = math.nan
        self.grondaankoop_makkelijk = math.nan
        self.grondaankoop_normaal = math.nan
        self.grondaankoop_moeilijk = math.nan

    def is_valid(self) -> bool:
        return all(
            _valid_float_prop(_prop)
            for _prop in super(StoringCostsExcludingTaxes, self).values()
        )


class KoswatCosts(KoswatConfigProtocol):
    eenheidsprijzen_section: UnitPrices
    kostendijkprofiel_section: DikeProfileCosts
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

        return all(
            valid_prop_config(_config) for _config in super(KoswatCosts, self).values()
        )
