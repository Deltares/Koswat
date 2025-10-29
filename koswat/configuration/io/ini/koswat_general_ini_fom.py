from __future__ import annotations

from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

from koswat.configuration.io.config_sections import (
    CofferdamReinforcementSectionFom,
    DikeProfileSectionFom,
    PipingWallReinforcementSectionFom,
    SoilReinforcementSectionFom,
    StabilitywallReinforcementSectionFom,
    VPSReinforcementSectionFom,
)
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class AnalysisSectionFom(KoswatIniFomProtocol):
    dike_selection_txt_file: Path
    dike_section_location_shp_file: Path
    input_profiles_json_dir: Path
    scenarios_ini_dir: Path
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
        _section.input_profiles_json_dir = Path(ini_config["dijksectie_invoer"])
        _section.scenarios_ini_dir = Path(ini_config["scenario_invoer"])
        _section.costs_ini_file = Path(ini_config["eenheidsprijzen"])
        _section.analysis_output_dir = Path(ini_config["uitvoerfolder"])
        _section.include_taxes = ini_config.getboolean("btw")
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
    custom: bool = False

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _types = ini_config.get("omgevingtypes", "").lower().strip().split(",")
        _section = cls(
            surroundings_database_dir=Path(ini_config["omgevingsdatabases"]),
            construction_distance=ini_config.getfloat("constructieafstand"),
            construction_buffer=ini_config.getfloat("constructieovergang"),
            waterside="buitendijks" in _types,
            buildings="bebouwing" in _types,
            railways="spoorwegen" in _types,
            waters="water" in _types,
            custom="custom" in _types,
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
    piping_wall_section: PipingWallReinforcementSectionFom
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
            dict(ini_config["Dijkprofiel"]), set_defaults=True
        )
        _general_ini.soil_measure_section = SoilReinforcementSectionFom.from_config(
            dict(ini_config["Grondmaatregel"]), set_defaults=True
        )
        _general_ini.vps_section = VPSReinforcementSectionFom.from_config(
            dict(ini_config["VerticalePipingOplossing"]), set_defaults=True
        )
        _general_ini.piping_wall_section = (
            PipingWallReinforcementSectionFom.from_config(
                dict(ini_config["Kwelscherm"]), set_defaults=True
            )
        )
        _general_ini.stability_wall_section = (
            StabilitywallReinforcementSectionFom.from_config(
                dict(ini_config["Stabiliteitswand"]), set_defaults=True
            )
        )
        _general_ini.cofferdam_section = CofferdamReinforcementSectionFom.from_config(
            dict(ini_config["Kistdam"]), set_defaults=True
        )
        _general_ini.surroundings_section = SurroundingsSectionFom.from_config(
            ini_config["Omgeving"]
        )
        _general_ini.infrastructuur_section = InfrastructureSectionFom.from_config(
            ini_config["Infrastructuur"]
        )
        return _general_ini
