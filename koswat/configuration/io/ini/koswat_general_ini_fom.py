from __future__ import annotations

import abc
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from koswat.configuration.models.koswat_general_settings import *
from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class AnalysisSectionFom(KoswatIniFomProtocol):
    dike_sections_selection_ini_file: Path  # Ini file
    dijksectie_ligging: Path  # shp file
    dike_sections_input_profiles_csv_file: Path  # csv file
    scenarios_dir: Path  # folder with ini files
    costs_ini_file: Path  # ini file
    analysis_output_dir: Path  # output folder
    include_taxes: bool

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.dike_sections_selection_ini_file = Path(
            ini_config["dijksecties_selectie"]
        )
        _section.dijksectie_ligging = Path(ini_config["dijksectie_ligging"])
        _section.dike_sections_input_profiles_csv_file = Path(
            ini_config["dijksectie_invoer"]
        )
        _section.scenarios_dir = Path(ini_config["scenario_invoer"])
        _section.costs_ini_file = Path(ini_config["eenheidsprijzen"])
        _section.analysis_output_dir = Path(ini_config["uitvoerfolder"])
        _section.include_taxes = ini_config.getboolean("btw")
        return _section


class DikeProfileSectionFom(DikeProfileSettings, KoswatIniFomProtocol):
    thickness_grass_layer: float
    thickness_clay_layer: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.thickness_grass_layer = ini_config.getfloat("dikte_graslaag")
        _section.thickness_clay_layer = ini_config.getfloat("dikte_kleilaag")
        return _section


class ReinforcementProfileSectionFomBase(
    ReinforcementProfileSettingsBase, KoswatIniFomProtocol, abc.ABC
):
    soil_storage_factor: StorageFactorEnum
    constructive_storage_factor: StorageFactorEnum
    purchased_soil_storage_factor: Optional[StorageFactorEnum]

    def _set_properties_from_dict(self, properties_dict: dict) -> None:
        self.soil_storage_factor = StorageFactorEnum[
            properties_dict["opslagfactor_grond"].upper()
        ]
        self.constructive_storage_factor = StorageFactorEnum[
            properties_dict.get(
                "opslagfactor_constructief", StorageFactorEnum.NORMAAL.name
            ).upper()
        ]
        self.purchased_soil_storage_factor = StorageFactorEnum[
            properties_dict.get(
                "opslagfactor_grondaankoop", StorageFactorEnum.NORMAAL.name
            ).upper()
        ]


class GrondmaatregelSectionFom(SoilSettings, ReinforcementProfileSectionFomBase):
    min_bermhoogte: float
    max_bermhoogte_factor: float
    factor_toename_bermhoogte: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_bermhoogte = ini_config.getfloat("min_bermhoogte")
        _section.max_bermhoogte_factor = ini_config.getfloat("max_bermhoogte_factor")
        _section.factor_toename_bermhoogte = float(
            ini_config["factor_toename_bermhoogte"]
        )
        return _section


class KwelschermSectionFom(PipingwallSettings, ReinforcementProfileSectionFomBase):
    min_lengte_kwelscherm: float
    overgang_cbwand_damwand: float
    max_lengte_kwelscherm: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_lengte_kwelscherm = ini_config.getfloat("min_lengte_kwelscherm")
        _section.overgang_cbwand_damwand = ini_config.getfloat(
            "overgang_cbwand_damwand"
        )
        _section.max_lengte_kwelscherm = ini_config.getfloat("max_lengte_kwelscherm")
        return _section


class StabiliteitswandSectionFom(
    StabilitywallSettings, ReinforcementProfileSectionFomBase
):
    versteiling_binnentalud: float
    min_lengte_stabiliteitswand: float
    overgang_damwand_diepwand: float
    max_lengte_stabiliteitswand: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.versteiling_binnentalud = ini_config.getfloat(
            "versteiling_binnentalud"
        )
        _section.min_lengte_stabiliteitswand = float(
            ini_config["min_lengte_stabiliteitswand"]
        )
        _section.overgang_damwand_diepwand = float(
            ini_config["overgang_damwand_diepwand"]
        )
        _section.max_lengte_stabiliteitswand = float(
            ini_config["max_lengte_stabiliteitswand"]
        )
        return _section


class KistdamSectionFom(CofferdamSettings, ReinforcementProfileSectionFomBase):
    min_lengte_kistdam: float
    max_lengte_kistdam: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_lengte_kistdam = ini_config.getfloat("min_lengte_kistdam")
        _section.max_lengte_kistdam = ini_config.getfloat("max_lengte_kistdam")
        return _section


class SurroundingsSectionFom(KoswatIniFomProtocol):
    omgevingsdatabases: Path  # Directory
    constructieafstand: float
    constructieovergang: float
    buitendijks: bool
    bebouwing: bool
    spoorwegen: bool
    water: bool

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.omgevingsdatabases = Path(ini_config["omgevingsdatabases"])
        _section.constructieafstand = ini_config.getfloat("constructieafstand")
        _section.constructieovergang = ini_config.getfloat("constructieovergang")
        _section.buitendijks = ini_config.getboolean("buitendijks")
        _section.bebouwing = ini_config.getboolean("bebouwing")
        _section.spoorwegen = ini_config.getboolean("spoorwegen")
        _section.water = ini_config.getboolean("water")
        return _section


class InfrastructuurSectionFom(InfrastructuurSettings, KoswatIniFomProtocol):
    infrastructuur: bool
    opslagfactor_wegen: StorageFactorEnum
    infrakosten_0dh: InfraCostsEnum
    buffer_buitendijks: float
    wegen_klasse2_breedte: float
    wegen_klasse24_breedte: float
    wegen_klasse47_breedte: float
    wegen_klasse7_breedte: float
    wegen_onbekend_breedte: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.infrastructuur = ini_config.getboolean("infrastructuur")
        _section.opslagfactor_wegen = StorageFactorEnum[
            ini_config["opslagfactor_wegen"].upper()
        ]
        _section.infrakosten_0dh = InfraCostsEnum[ini_config["infrakosten_0dh"].upper()]
        _section.buffer_buitendijks = ini_config.getfloat("buffer_buitendijks")
        _section.wegen_klasse2_breedte = ini_config.getfloat("wegen_klasse2_breedte")
        _section.wegen_klasse24_breedte = ini_config.getfloat("wegen_klasse24_breedte")
        _section.wegen_klasse47_breedte = ini_config.getfloat("wegen_klasse47_breedte")
        _section.wegen_klasse7_breedte = ini_config.getfloat("wegen_klasse7_breedte")
        _section.wegen_onbekend_breedte = ini_config.getfloat("wegen_onbekend_breedte")
        return _section


class KoswatGeneralIniFom(KoswatIniFomProtocol):
    analyse_section: AnalysisSectionFom
    dijkprofiel_section: DikeProfileSectionFom
    grondmaatregel_section: GrondmaatregelSectionFom
    kwelscherm_section: KwelschermSectionFom
    stabiliteitswand_section: StabiliteitswandSectionFom
    kistdam_section: KistdamSectionFom
    surroundings_section: SurroundingsSectionFom
    infrastructuur_section: InfrastructuurSectionFom

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _general_ini = cls()

        _general_ini.analyse_section = AnalysisSectionFom.from_config(
            ini_config["Analyse"]
        )
        _general_ini.dijkprofiel_section = DikeProfileSectionFom.from_config(
            ini_config["Dijkprofiel"]
        )
        _general_ini.grondmaatregel_section = GrondmaatregelSectionFom.from_config(
            ini_config["Grondmaatregel"]
        )
        _general_ini.kwelscherm_section = KwelschermSectionFom.from_config(
            ini_config["Kwelscherm"]
        )
        _general_ini.stabiliteitswand_section = StabiliteitswandSectionFom.from_config(
            ini_config["Stabiliteitswand"]
        )
        _general_ini.kistdam_section = KistdamSectionFom.from_config(
            ini_config["Kistdam"]
        )
        _general_ini.surroundings_section = SurroundingsSectionFom.from_config(
            ini_config["Omgeving"]
        )
        _general_ini.infrastructuur_section = InfrastructuurSectionFom.from_config(
            ini_config["Infrastructuur"]
        )
        return _general_ini
