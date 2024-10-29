from configparser import ConfigParser

from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class UnitPricesSectionFom(KoswatIniFomProtocol):
    price_level: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.price_level = ini_config.getint("prijspeil")
        return _section


class DikeProfileCostsSectionFom(KoswatIniFomProtocol):
    construction_grass_layer_m3: float
    construction_clay_layer_m3: float
    construction_sand_m3: float
    reuse_grass_layer_m3: float
    reuse_sand_m3: float
    dispose_material_m3: float
    profile_grass_layer_m2: float
    profile_clay_layer_m2: float
    profile_sand_m2: float
    process_ground_level_surface_m2: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.construction_grass_layer_m3 = ini_config.getfloat("aanleg_graslaag_m3")
        _section.construction_clay_layer_m3 = ini_config.getfloat("aanleg_kleilaag_m3")
        _section.construction_sand_m3 = ini_config.getfloat("aanleg_kern_m3")
        _section.reuse_grass_layer_m3 = ini_config.getfloat("hergebruik_graslaag_m3")
        _section.reuse_sand_m3 = ini_config.getfloat("hergebruik_kern_m3")
        _section.dispose_material_m3 = ini_config.getfloat("afvoeren_materiaal_m3")
        _section.profile_grass_layer_m2 = ini_config.getfloat("profileren_graslaag_m2")
        _section.profile_clay_layer_m2 = ini_config.getfloat("profileren_kleilaag_m2")
        _section.profile_sand_m2 = ini_config.getfloat("profileren_kern_m2")
        _section.process_ground_level_surface_m2 = ini_config.getfloat(
            "bewerken_maaiveld_m2"
        )
        return _section


class InfrastructureCostsSectionFom(KoswatIniFomProtocol):
    roads_class2_removal: float
    roads_class24_removal: float
    roads_class47_removal: float
    roads_class7_removal: float
    roads_unknown_removal: float
    roads_class2_construction: float
    roads_class24_construction: float
    roads_class47_construction: float
    roads_class7_construction: float
    roads_unknown_construction: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.roads_class2_removal = ini_config.getfloat("wegen_klasse2_verwijderen")
        _section.roads_class24_removal = ini_config.getfloat(
            "wegen_klasse24_verwijderen"
        )
        _section.roads_class47_removal = ini_config.getfloat(
            "wegen_klasse47_verwijderen"
        )
        _section.roads_class7_removal = ini_config.getfloat("wegen_klasse7_verwijderen")
        _section.roads_unknown_removal = ini_config.getfloat(
            "wegen_onbekend_verwijderen"
        )
        _section.roads_class2_construction = ini_config.getfloat("wegen_klasse2_aanleg")
        _section.roads_class24_construction = ini_config.getfloat(
            "wegen_klasse24_aanleg"
        )
        _section.roads_class47_construction = ini_config.getfloat(
            "wegen_klasse47_aanleg"
        )
        _section.roads_class7_construction = ini_config.getfloat("wegen_klasse7_aanleg")
        _section.roads_unknown_construction = ini_config.getfloat(
            "wegen_onbekend_aanleg"
        )
        return _section


class SurtaxCostsSectionFom(KoswatIniFomProtocol):
    soil_easy: float
    soil_normal: float
    soil_hard: float
    constructive_easy: float
    constructive_normal: float
    constructive_hard: float
    road_easy: float
    roads_normal: float
    roads_hard: float
    land_purchase_easy: float
    land_purchase_normal: float
    land_purchase_hard: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.soil_easy = ini_config.getfloat("grond_makkelijk")
        _section.soil_normal = ini_config.getfloat("grond_normaal")
        _section.soil_hard = ini_config.getfloat("grond_moeilijk")
        _section.constructive_easy = ini_config.getfloat("constructief_makkelijk")
        _section.constructive_normal = ini_config.getfloat("constructief_normaal")
        _section.constructive_hard = ini_config.getfloat("constructief_moeilijk")
        _section.road_easy = ini_config.getfloat("wegen_makkelijk")
        _section.roads_normal = ini_config.getfloat("wegen_normaal")
        _section.roads_hard = ini_config.getfloat("wegen_moeilijk")
        _section.land_purchase_easy = ini_config.getfloat("grondaankoop_makkelijk")
        _section.land_purchase_normal = ini_config.getfloat("grondaankoop_normaal")
        _section.land_purchase_hard = ini_config.getfloat("grondaankoop_moeilijk")
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
