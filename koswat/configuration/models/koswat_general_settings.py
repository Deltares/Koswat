from __future__ import annotations

import abc
import enum
from pathlib import Path
from typing import Optional

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.io.ini.koswat_ini_fom_protocol import KoswatConfigProtocol


class StorageFactorEnum(enum.Enum):
    MAKKELIJK = 0
    NORMAAL = 1
    MOEILIJK = 2


class InfraCostsEnum(enum.Enum):
    GEEN = 0
    HERSTEL = 1
    VERVANG = 2


class Analysis(KoswatConfigProtocol):
    dijksecties_selectie: Path  # Ini file
    dijksectie_ligging: Path  # shp file
    dijksectie_invoer: Path  # csv file
    scenario_invoer: Path  # folder with ini files
    eenheidsprijzen: Path  # ini file
    uitvoerfolder: Path  # output folder
    btw: bool


class DikeProfile(KoswatConfigProtocol):
    dikte_graslaag: float
    dikte_kleilaag: float


class ReinforcementProfile(KoswatConfigProtocol, abc.ABC):
    opslagfactor_grond: StorageFactorEnum
    opslagfactor_constructief: StorageFactorEnum
    opslagfactor_grondaankoop: Optional[StorageFactorEnum]


class Grondmaatregel(ReinforcementProfile):
    min_bermhoogte: float
    max_bermhoogte_factor: float
    factor_toename_bermhoogte: float


class Kwelscherm(ReinforcementProfile):
    min_lengte_kwelscherm: float
    overgang_cbwand_damwand: float
    max_lengte_kwelscherm: float


class Stabiliteits(ReinforcementProfile):
    versteiling_binnentalud: float
    min_lengte_stabiliteitswand: float
    overgang_damwand_diepwand: float
    max_lengte_stabiliteitswand: float


class Kistdam(ReinforcementProfile):
    min_lengte_kistdam: float
    max_lengte_kistdam: float


class Omgeving(KoswatConfigProtocol):
    omgevingsdatabases: Path  # Directory
    constructieafstand: float
    constructieovergang: float
    buitendijks: bool
    bebouwing: bool
    spoorwegen: bool
    water: bool


class Infrastructuur(KoswatConfigProtocol):
    infrastructuur: bool
    opslagfactor_wegen: StorageFactorEnum
    infrakosten_0dh: InfraCostsEnum
    buffer_buitendijks: float
    wegen_klasse2_breedte: float
    wegen_klasse24_breedte: float
    wegen_klasse47_breedte: float
    wegen_klasse7_breedte: float
    wegen_onbekend_breedte: float


class KoswatGeneralSettings(KoswatConfigProtocol):
    analyse_section: Analysis
    dijkprofiel_section: DikeProfile
    grondmaatregel_section: Grondmaatregel
    kwelscherm_section: Kwelscherm
    stabiliteitswand_section: Stabiliteits
    kistdam_section: Kistdam
    omgeving_section: Omgeving
    infrastructuur_section: Infrastructuur
