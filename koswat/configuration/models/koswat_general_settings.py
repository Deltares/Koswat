from __future__ import annotations

import abc
import enum
import math
from pathlib import Path
from typing import List, Optional

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.models.koswat_costs import KoswatCosts
from koswat.configuration.models.koswat_dike_selection import KoswatDikeSelection
from koswat.configuration.models.koswat_scenario import KoswatScenario


class StorageFactorEnum(enum.Enum):
    MAKKELIJK = 0
    NORMAAL = 1
    MOEILIJK = 2


class InfraCostsEnum(enum.Enum):
    GEEN = 0
    HERSTEL = 1
    VERVANG = 2


class AnalysisSettings(KoswatConfigProtocol):
    dike_selection: KoswatDikeSelection
    scenarios: List[KoswatScenario]
    costs: KoswatCosts
    analysis_output: Path  # output folder
    dijksectie_ligging: Path  # shp file
    dijksectie_invoer: Path  # csv file
    include_taxes: bool

    def __init__(self) -> None:
        self.dijksecties_selectie

    def is_valid(self) -> bool:
        pass


class DikeProfileSettings(KoswatConfigProtocol):
    thickness_grass_layer: float
    thickness_clay_layer: float

    def is_valid(self) -> bool:
        return not math.isnan(self.thickness_grass_layer) and not math.isnan(
            self.thickness_clay_layer
        )


class ReinforcementProfileSettingsBase(KoswatConfigProtocol, abc.ABC):
    soil_storage_factor: StorageFactorEnum
    constructive_storage_factor: StorageFactorEnum
    purchased_soil_storage_factor: Optional[StorageFactorEnum]

    def is_valid(self) -> bool:
        pass


class GrondmaatregelSettings(ReinforcementProfileSettingsBase):
    min_bermhoogte: float
    max_bermhoogte_factor: float
    factor_toename_bermhoogte: float

    def is_valid(self) -> bool:
        pass


class KwelschermSettings(ReinforcementProfileSettingsBase):
    min_lengte_kwelscherm: float
    overgang_cbwand_damwand: float
    max_lengte_kwelscherm: float

    def is_valid(self) -> bool:
        pass


class StabiliteitswandSettings(ReinforcementProfileSettingsBase):
    versteiling_binnentalud: float
    min_lengte_stabiliteitswand: float
    overgang_damwand_diepwand: float
    max_lengte_stabiliteitswand: float

    def is_valid(self) -> bool:
        pass


class KistdamSettings(ReinforcementProfileSettingsBase):
    min_lengte_kistdam: float
    max_lengte_kistdam: float

    def is_valid(self) -> bool:
        pass


class OmgevingSettings(KoswatConfigProtocol):
    omgevingsdatabases: Path  # Directory
    constructieafstand: float
    constructieovergang: float
    buitendijks: bool
    bebouwing: bool
    spoorwegen: bool
    water: bool

    def is_valid(self) -> bool:
        pass


class InfrastructuurSettings(KoswatConfigProtocol):
    infrastructuur: bool
    opslagfactor_wegen: StorageFactorEnum
    infrakosten_0dh: InfraCostsEnum
    buffer_buitendijks: float
    wegen_klasse2_breedte: float
    wegen_klasse24_breedte: float
    wegen_klasse47_breedte: float
    wegen_klasse7_breedte: float
    wegen_onbekend_breedte: float

    def is_valid(self) -> bool:
        pass
