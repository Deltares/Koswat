from __future__ import annotations

import abc
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class AnalysisSectionFom(KoswatIniFomProtocol):
    dike_selection_txt_file: Path
    dike_section_location_shp_file: Path
    input_profiles_csv_file: Path
    scenarios_ini_file: Path
    costs_ini_file: Path
    analysis_output_dir: Path
    include_taxes: bool

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> AnalysisSectionFom:
        """
        Converts the values from a default koswat ini  file containing an Analyse section into a an instance of `AnalysisSectionFom`

        Args:
            ini_config (ConfigParser): Parsed ini object.

        Returns:
            AnalysisSectionFom: Valid instance of an `AnalysisSectionFom`.
        """
        _section = cls()
        _section.dike_selection_txt_file = Path(ini_config["dijksecties_selectie"])
        _section.dike_section_location_shp_file = Path(ini_config["dijksectie_ligging"])
        _section.input_profiles_csv_file = Path(ini_config["dijksectie_invoer"])
        _section.scenarios_ini_file = Path(ini_config["scenario_invoer"])
        _section.costs_ini_file = Path(ini_config["eenheidsprijzen"])
        _section.analysis_output_dir = Path(ini_config["uitvoerfolder"])
        _section.include_taxes = ini_config.getboolean("btw")
        return _section


class DikeProfileSectionFom(KoswatIniFomProtocol):
    thickness_grass_layer: float
    thickness_clay_layer: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.thickness_grass_layer = ini_config.getfloat("dikte_graslaag")
        _section.thickness_clay_layer = ini_config.getfloat("dikte_kleilaag")
        return _section


class ReinforcementProfileSectionFomBase(KoswatIniFomProtocol, abc.ABC):
    soil_surtax_factor: SurtaxFactorEnum

    def _set_properties_from_dict(self, properties_dict: dict) -> None:
        self.soil_surtax_factor = SurtaxFactorEnum[
            properties_dict["opslagfactor_grond"].upper()
        ]


class SoilReinforcementSectionFom(ReinforcementProfileSectionFomBase):
    min_berm_height: float
    max_berm_height_factor: float
    factor_increase_berm_height: float
    land_purchase_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_berm_height = ini_config.getfloat("min_bermhoogte")
        _section.max_berm_height_factor = ini_config.getfloat("max_bermhoogte_factor")
        _section.factor_increase_berm_height = ini_config.getfloat(
            "factor_toename_bermhoogte"
        )
        _section.land_purchase_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_grondaankoop", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        return _section


class VPSReinforcementSectionFom(ReinforcementProfileSectionFomBase):
    polderside_berm_width_vps: float
    constructive_surtax_factor: float
    land_purchase_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.polderside_berm_width_vps = ini_config.getfloat(
            "binnen_berm_breedte_vps"
        )
        _section.constructive_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_constructief", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        _section.land_purchase_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_grondaankoop", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        return _section


class PipingwallReinforcementSectionFom(ReinforcementProfileSectionFomBase):
    min_length_piping_wall: float
    transition_cbwall_sheetpile: float
    max_length_piping_wall: float
    constructive_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_length_piping_wall = ini_config.getfloat("min_lengte_kwelscherm")
        _section.transition_cbwall_sheetpile = ini_config.getfloat(
            "overgang_cbwand_damwand"
        )
        _section.max_length_piping_wall = ini_config.getfloat("max_lengte_kwelscherm")
        _section.constructive_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_constructief", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        _section.land_purchase_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_grondaankoop", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        return _section


class StabilitywallReinforcementSectionFom(ReinforcementProfileSectionFomBase):
    steepening_polderside_slope: float
    min_length_stability_wall: float
    transition_sheetpile_diaphragm_wall: float
    max_length_stability_wall: float
    constructive_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.steepening_polderside_slope = ini_config.getfloat(
            "versteiling_binnentalud"
        )
        _section.min_length_stability_wall = ini_config.getfloat(
            "min_lengte_stabiliteitswand"
        )
        _section.transition_sheetpile_diaphragm_wall = ini_config.getfloat(
            "overgang_damwand_diepwand"
        )
        _section.max_length_stability_wall = ini_config.getfloat(
            "max_lengte_stabiliteitswand"
        )
        _section.constructive_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_constructief", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        _section.land_purchase_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_grondaankoop", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        return _section


class CofferdamReinforcementSectionFom(ReinforcementProfileSectionFomBase):
    min_length_cofferdam: float
    max_length_cofferdam: float
    constructive_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_length_cofferdam = ini_config.getfloat("min_lengte_kistdam")
        _section.max_length_cofferdam = ini_config.getfloat("max_lengte_kistdam")
        _section.constructive_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_constructief", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        return _section


@dataclass
class SurroundingsSectionFom(KoswatIniFomProtocol):
    surroundings_database_dir: Path
    construction_distance: float
    construction_buffer: float
    waterside: bool
    buildings: bool
    railways: bool
    waters: bool

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls(
            surroundings_database_dir=Path(ini_config["omgevingsdatabases"]),
            construction_distance=ini_config.getfloat("constructieafstand"),
            construction_buffer=ini_config.getfloat("constructieovergang"),
            waterside=ini_config.getboolean("buitendijks"),
            buildings=ini_config.getboolean("bebouwing"),
            railways=ini_config.getboolean("spoorwegen"),
            waters=ini_config.getboolean("water"),
        )
        return _section


@dataclass
class InfrastructureSectionFom(KoswatIniFomProtocol):
    infrastructure: bool
    surtax_factor_roads: SurtaxFactorEnum
    infrastructure_costs_0dh: InfraCostsEnum
    buffer_waterside: float
    roads_class2_width: float
    roads_class24_width: float
    roads_class47_width: float
    roads_class7_width: float
    roads_unknown_width: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        return cls(
            infrastructure=ini_config.getboolean("infrastructuur"),
            surtax_factor_roads=SurtaxFactorEnum[
                ini_config["opslagfactor_wegen"].upper()
            ],
            infrastructure_costs_0dh=InfraCostsEnum[
                ini_config["infrakosten_0dh"].upper()
            ],
            buffer_waterside=ini_config.getfloat("buffer_buitendijks"),
            roads_class2_width=ini_config.getfloat("wegen_klasse2_breedte"),
            roads_class24_width=ini_config.getfloat("wegen_klasse24_breedte"),
            roads_class47_width=ini_config.getfloat("wegen_klasse47_breedte"),
            roads_class7_width=ini_config.getfloat("wegen_klasse7_breedte"),
            roads_unknown_width=ini_config.getfloat("wegen_onbekend_breedte"),
        )


class KoswatGeneralIniFom(KoswatIniFomProtocol):
    analysis_section: AnalysisSectionFom
    dike_profile_section: DikeProfileSectionFom
    soil_measure_section: SoilReinforcementSectionFom
    vps_section: VPSReinforcementSectionFom
    piping_wall_section: PipingwallReinforcementSectionFom
    stability_wall_section: StabilitywallReinforcementSectionFom
    cofferdam_section: CofferdamReinforcementSectionFom
    surroundings_section: SurroundingsSectionFom
    infrastructuur_section: InfrastructureSectionFom

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _general_ini = cls()

        _general_ini.analysis_section = AnalysisSectionFom.from_config(
            ini_config["Analyse"]
        )
        _general_ini.dike_profile_section = DikeProfileSectionFom.from_config(
            ini_config["Dijkprofiel"]
        )
        _general_ini.soil_measure_section = SoilReinforcementSectionFom.from_config(
            ini_config["Grondmaatregel"]
        )
        _general_ini.vps_section = VPSReinforcementSectionFom.from_config(
            ini_config["VerticalePipingOplossing"]
        )
        _general_ini.piping_wall_section = (
            PipingwallReinforcementSectionFom.from_config(ini_config["Kwelscherm"])
        )
        _general_ini.stability_wall_section = (
            StabilitywallReinforcementSectionFom.from_config(
                ini_config["Stabiliteitswand"]
            )
        )
        _general_ini.cofferdam_section = CofferdamReinforcementSectionFom.from_config(
            ini_config["Kistdam"]
        )
        _general_ini.surroundings_section = SurroundingsSectionFom.from_config(
            ini_config["Omgeving"]
        )
        _general_ini.infrastructuur_section = InfrastructureSectionFom.from_config(
            ini_config["Infrastructuur"]
        )
        return _general_ini
