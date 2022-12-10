from __future__ import annotations

import abc
import enum
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class StorageFactorEnum(enum.Enum):
    MAKKELIJK = 0
    NORMAAL = 1
    MOEILIJK = 2


class InfraCostsEnum(enum.Enum):
    GEEN = 0
    HERSTEL = 1
    VERVANG = 2


class AnalysisSection(KoswatIniFomProtocol):
    dijksecties_selectie: Path  # Ini file
    dijksectie_ligging: Path  # shp file
    dijksectie_invoer: Path  # csv file
    scenario_invoer: Path  # folder with ini files
    eenheidsprijzen: Path  # ini file
    uitvoerfolder: Path  # output folder
    btw: bool

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.dijksecties_selectie = Path(ini_config["dijksecties_selectie"])
        _section.dijksectie_ligging = Path(ini_config["dijksectie_ligging"])
        _section.dijksectie_invoer = Path(ini_config["dijksectie_invoer"])
        _section.scenario_invoer = Path(ini_config["scenario_invoer"])
        _section.eenheidsprijzen = Path(ini_config["eenheidsprijzen"])
        _section.uitvoerfolder = Path(ini_config["uitvoerfolder"])
        _section.btw = ini_config.getboolean("btw")
        return _section


class DikeProfileSection(KoswatIniFomProtocol):
    dikte_graslaag: float
    dikte_kleilaag: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.dikte_graslaag = ini_config.getfloat("dikte_graslaag")
        _section.dikte_kleilaag = ini_config.getfloat("dikte_kleilaag")
        return _section


class ReinforcementProfileSection(KoswatIniFomProtocol, abc.ABC):
    opslagfactor_grond: StorageFactorEnum
    opslagfactor_constructief: StorageFactorEnum
    opslagfactor_grondaankoop: Optional[StorageFactorEnum]

    def _set_properties_from_dict(self, properties_dict: dict) -> None:
        self.opslagfactor_grond = StorageFactorEnum[
            properties_dict["opslagfactor_grond"].upper()
        ]
        self.opslagfactor_constructief = StorageFactorEnum[
            properties_dict.get(
                "opslagfactor_constructief", StorageFactorEnum.NORMAAL.name
            ).upper()
        ]
        self.opslagfactor_grondaankoop = StorageFactorEnum[
            properties_dict.get(
                "opslagfactor_grondaankoop", StorageFactorEnum.NORMAAL.name
            ).upper()
        ]


class GrondmaatregelSection(ReinforcementProfileSection):
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


class KwelschermSection(ReinforcementProfileSection):
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


class StabiliteitswandSection(ReinforcementProfileSection):
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


class KistdamSection(ReinforcementProfileSection):
    min_lengte_kistdam: float
    max_lengte_kistdam: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_lengte_kistdam = ini_config.getfloat("min_lengte_kistdam")
        _section.max_lengte_kistdam = ini_config.getfloat("max_lengte_kistdam")
        return _section


class OmgevingSection(KoswatIniFomProtocol):
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


class InfrastructuurSection(KoswatIniFomProtocol):
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
    analyse_section: AnalysisSection
    dijkprofiel_section: DikeProfileSection
    grondmaatregel_section: GrondmaatregelSection
    kwelscherm_section: KwelschermSection
    stabiliteitswand_section: StabiliteitswandSection
    kistdam_section: KistdamSection
    omgeving_section: OmgevingSection
    infrastructuur_section: InfrastructuurSection

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _general_ini = cls()

        _general_ini.analyse_section = AnalysisSection.from_config(ini_config["Analyse"])
        _general_ini.dijkprofiel_section = DikeProfileSection.from_config(
            ini_config["Dijkprofiel"]
        )
        _general_ini.grondmaatregel_section = GrondmaatregelSection.from_config(
            ini_config["Grondmaatregel"]
        )
        _general_ini.kwelscherm_section = KwelschermSection.from_config(
            ini_config["Kwelscherm"]
        )
        _general_ini.stabiliteitswand_section = StabiliteitswandSection.from_config(
            ini_config["Stabiliteitswand"]
        )
        _general_ini.kistdam_section = KistdamSection.from_config(ini_config["Kistdam"])
        _general_ini.omgeving_section = OmgevingSection.from_config(
            ini_config["Omgeving"]
        )
        _general_ini.infrastructuur_section = InfrastructuurSection.from_config(
            ini_config["Infrastructuur"]
        )
        return _general_ini
