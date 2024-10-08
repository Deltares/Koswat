from configparser import ConfigParser

from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class UnitPricesSectionFom(KoswatIniFomProtocol):
    prijspeil: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.prijspeil = ini_config.getint("prijspeil")
        return _section


class DikeProfileCostsSectionFom(KoswatIniFomProtocol):
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

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.aanleg_graslaag_m3 = ini_config.getfloat("aanleg_graslaag_m3")
        _section.aanleg_kleilaag_m3 = ini_config.getfloat("aanleg_kleilaag_m3")
        _section.aanleg_kern_m3 = ini_config.getfloat("aanleg_kern_m3")
        _section.hergebruik_graslaag_m3 = ini_config.getfloat("hergebruik_graslaag_m3")
        _section.hergebruik_kern_m3 = ini_config.getfloat("hergebruik_kern_m3")
        _section.afvoeren_materiaal_m3 = ini_config.getfloat("afvoeren_materiaal_m3")
        _section.profileren_graslaag_m2 = ini_config.getfloat("profileren_graslaag_m2")
        _section.profileren_kleilaag_m2 = ini_config.getfloat("profileren_kleilaag_m2")
        _section.profileren_kern_m2 = ini_config.getfloat("profileren_kern_m2")
        _section.bewerken_maaiveld_m2 = ini_config.getfloat("bewerken_maaiveld_m2")
        return _section


class InfrastructureCostsSectionFom(KoswatIniFomProtocol):
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

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.wegen_klasse2_verwijderen = ini_config.getfloat(
            "wegen_klasse2_verwijderen"
        )
        _section.wegen_klasse24_verwijderen = ini_config.getfloat(
            "wegen_klasse24_verwijderen"
        )
        _section.wegen_klasse47_verwijderen = ini_config.getfloat(
            "wegen_klasse47_verwijderen"
        )
        _section.wegen_klasse7_verwijderen = ini_config.getfloat(
            "wegen_klasse7_verwijderen"
        )
        _section.wegen_onbekend_verwijderen = ini_config.getfloat(
            "wegen_onbekend_verwijderen"
        )
        _section.wegen_klasse2_aanleg = ini_config.getfloat("wegen_klasse2_aanleg")
        _section.wegen_klasse24_aanleg = ini_config.getfloat("wegen_klasse24_aanleg")
        _section.wegen_klasse47_aanleg = ini_config.getfloat("wegen_klasse47_aanleg")
        _section.wegen_klasse7_aanleg = ini_config.getfloat("wegen_klasse7_aanleg")
        _section.wegen_onbekend_aanleg = ini_config.getfloat("wegen_onbekend_aanleg")
        return _section


class SurtaxCostsSectionFom(KoswatIniFomProtocol):
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

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.grond_makkelijk = ini_config.getfloat("grond_makkelijk")
        _section.grond_normaal = ini_config.getfloat("grond_normaal")
        _section.grond_moeilijk = ini_config.getfloat("grond_moeilijk")
        _section.constructief_makkelijk = ini_config.getfloat("constructief_makkelijk")
        _section.constructief_normaal = ini_config.getfloat("constructief_normaal")
        _section.constructief_moeilijk = ini_config.getfloat("constructief_moeilijk")
        _section.wegen_makkelijk = ini_config.getfloat("wegen_makkelijk")
        _section.wegen_normaal = ini_config.getfloat("wegen_normaal")
        _section.wegen_moeilijk = ini_config.getfloat("wegen_moeilijk")
        _section.grondaankoop_makkelijk = ini_config.getfloat("grondaankoop_makkelijk")
        _section.grondaankoop_normaal = ini_config.getfloat("grondaankoop_normaal")
        _section.grondaankoop_moeilijk = ini_config.getfloat("grondaankoop_moeilijk")
        return _section


class ConstructionCostsSectionFom(KoswatIniFomProtocol):
    c_factor: float
    d_factor: float
    z_factor: float
    f_factor: float
    g_factor: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.c_factor = ini_config.getfloat("c")
        _section.d_factor = ini_config.getfloat("d")
        _section.z_factor = ini_config.getfloat("z")
        _section.f_factor = ini_config.getfloat("f")
        _section.g_factor = ini_config.getfloat("g")
        return _section


class KoswatCostsIniFom(KoswatIniFomProtocol):
    unit_prices_section: UnitPricesSectionFom
    dike_profile_costs_section: DikeProfileCostsSectionFom
    infrastructure_costs_section: InfrastructureCostsSectionFom
    surtax_costs_incl_tax_section: SurtaxCostsSectionFom
    surtax_costs_excl_tax_section: SurtaxCostsSectionFom
    construction_cost_cb_wall: ConstructionCostsSectionFom
    construction_cost_vzg: ConstructionCostsSectionFom
    construction_cost_damwall_unanchored: ConstructionCostsSectionFom
    construction_cost_damwall_anchored: ConstructionCostsSectionFom
    construction_cost_deep_wall: ConstructionCostsSectionFom
    construction_cost_cofferdam: ConstructionCostsSectionFom

    @classmethod
    def from_config(cls, ini_dict: ConfigParser) -> KoswatIniFomProtocol:
        _ini_fom = cls()
        _ini_fom.unit_prices_section = UnitPricesSectionFom.from_config(
            ini_dict["Eenheidsprijzen"]
        )
        _ini_fom.dike_profile_costs_section = DikeProfileCostsSectionFom.from_config(
            ini_dict["KostenDijkprofiel"]
        )
        _ini_fom.infrastructure_costs_section = (
            InfrastructureCostsSectionFom.from_config(ini_dict["KostenInfrastructuur"])
        )
        _ini_fom.surtax_costs_incl_tax_section = SurtaxCostsSectionFom.from_config(
            ini_dict["KostenOpslagfactorenInclBTW"]
        )
        _ini_fom.surtax_costs_excl_tax_section = SurtaxCostsSectionFom.from_config(
            ini_dict["KostenOpslagfactorenExclBTW"]
        )
        _ini_fom.construction_cost_vzg = ConstructionCostsSectionFom.from_config(
            ini_dict["KostenVerticaalZanddichtGeotextiel"]
        )
        _ini_fom.construction_cost_cb_wall = ConstructionCostsSectionFom.from_config(
            ini_dict["KostenCBwand"]
        )
        _ini_fom.construction_cost_damwall_unanchored = (
            ConstructionCostsSectionFom.from_config(
                ini_dict["KostenDamwandOnverankerd"]
            )
        )
        _ini_fom.construction_cost_damwall_anchored = (
            ConstructionCostsSectionFom.from_config(ini_dict["KostenDamwandVerankerd"])
        )
        _ini_fom.construction_cost_deep_wall = ConstructionCostsSectionFom.from_config(
            ini_dict["KostenDiepwand"]
        )
        _ini_fom.construction_cost_cofferdam = ConstructionCostsSectionFom.from_config(
            ini_dict["KostenKistdam"]
        )
        return _ini_fom
