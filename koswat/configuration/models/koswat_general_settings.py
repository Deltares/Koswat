from __future__ import annotations

import abc
import enum
import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.models.koswat_costs import KoswatCosts
from koswat.configuration.models.koswat_dike_selection import KoswatDikeSelection
from koswat.configuration.models.koswat_scenario import KoswatScenario
from koswat.dike.material.koswat_material_type import KoswatMaterialType


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
        self.dike_selection = None
        self.scenarios = None
        self.costs = None
        self.analysis_output = None
        self.dijksectie_ligging = None
        self.dijksectie_invoer = None
        self.include_taxes = True  # Default value.

    def is_valid(self) -> bool:
        return (
            self.dike_selection.is_valid()
            and all(_s.is_valid() for _s in self.scenarios)
            and self.costs.is_valid()
            and self.analysis_output is not None
            and self.dijksectie_ligging.is_file()
            and self.dijksectie_invoer.is_file()
        )


class DikeProfileSettings(KoswatConfigProtocol):
    thickness_grass_layer: float
    thickness_clay_layer: float

    def is_valid(self) -> bool:
        return not math.isnan(self.thickness_grass_layer) and not math.isnan(
            self.thickness_clay_layer
        )

    def get_material_thickness(self) -> List[dict]:
        
        return dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[
                dict(material=KoswatMaterialType.GRASS, depth=self.thickness_grass_layer),
            dict(material=KoswatMaterialType.CLAY, depth=self.thickness_clay_layer),
            ]
        )


class ReinforcementProfileSettingsBase(KoswatConfigProtocol, abc.ABC):
    soil_storage_factor: StorageFactorEnum
    constructive_storage_factor: StorageFactorEnum
    purchased_soil_storage_factor: Optional[StorageFactorEnum]

    def is_valid(self) -> bool:
        return (
            self.soil_storage_factor is not None
            and self.constructive_storage_factor is not None
        )


class SoilSettings(ReinforcementProfileSettingsBase):
    min_bermhoogte: float
    max_bermhoogte_factor: float
    factor_toename_bermhoogte: float

    def __init__(self) -> None:
        self.soil_storage_factor = None  # So that we can check they actually get set.
        self.constructive_storage_factor = (
            None  # So that we can check they actually get set.
        )
        self.purchased_soil_storage_factor = (
            None  # So that we can check they actually get set.
        )
        self.min_bermhoogte = math.nan
        self.max_bermhoogte_factor = math.nan
        self.factor_toename_bermhoogte = math.nan

    def is_valid(self) -> bool:
        _reinforcent_base_validation = super(
            ReinforcementProfileSettingsBase, self
        ).is_valid()
        return (
            _reinforcent_base_validation
            and not math.isnan(self.min_bermhoogte)
            and not math.isnan(self.max_bermhoogte_factor)
            and not math.isnan(self.factor_toename_bermhoogte)
        )


class PipingwallSettings(ReinforcementProfileSettingsBase):
    min_lengte_kwelscherm: float
    overgang_cbwand_damwand: float
    max_lengte_kwelscherm: float

    def __init__(self) -> None:
        self.soil_storage_factor = None  # So that we can check they actually get set.
        self.constructive_storage_factor = (
            None  # So that we can check they actually get set.
        )
        self.purchased_soil_storage_factor = (
            None  # So that we can check they actually get set.
        )
        self.min_lengte_kwelscherm = math.nan
        self.overgang_cbwand_damwand = math.nan
        self.max_lengte_kwelscherm = math.nan

    def is_valid(self) -> bool:
        _reinforcent_base_validation = super(
            ReinforcementProfileSettingsBase, self
        ).is_valid()
        return (
            _reinforcent_base_validation
            and not math.isnan(self.min_lengte_kwelscherm)
            and not math.isnan(self.overgang_cbwand_damwand)
            and not math.isnan(self.max_lengte_kwelscherm)
        )


class StabilitywallSettings(ReinforcementProfileSettingsBase):
    versteiling_binnentalud: float
    min_lengte_stabiliteitswand: float
    overgang_damwand_diepwand: float
    max_lengte_stabiliteitswand: float

    def __init__(self) -> None:
        self.soil_storage_factor = None  # So that we can check they actually get set.
        self.constructive_storage_factor = (
            None  # So that we can check they actually get set.
        )
        self.purchased_soil_storage_factor = (
            None  # So that we can check they actually get set.
        )
        self.versteiling_binnentalud = math.nan
        self.min_lengte_stabiliteitswand = math.nan
        self.overgang_damwand_diepwand = math.nan
        self.max_lengte_stabiliteitswand = math.nan

    def is_valid(self) -> bool:
        _reinforcent_base_validation = super(
            ReinforcementProfileSettingsBase, self
        ).is_valid()
        return (
            _reinforcent_base_validation
            and not math.isnan(self.versteiling_binnentalud)
            and not math.isnan(self.min_lengte_stabiliteitswand)
            and not math.isnan(self.overgang_damwand_diepwand)
            and not math.isnan(self.max_lengte_stabiliteitswand)
        )


class CofferdamSettings(ReinforcementProfileSettingsBase):
    min_lengte_kistdam: float
    max_lengte_kistdam: float

    def __init__(self) -> None:
        self.soil_storage_factor = None  # So that we can check they actually get set.
        self.constructive_storage_factor = (
            None  # So that we can check they actually get set.
        )
        self.purchased_soil_storage_factor = (
            None  # So that we can check they actually get set.
        )
        self.min_lengte_kistdam = math.nan
        self.max_lengte_kistdam = math.nan

    def is_valid(self) -> bool:
        _reinforcent_base_validation = super(
            ReinforcementProfileSettingsBase, self
        ).is_valid()
        return (
            _reinforcent_base_validation
            and not math.isnan(self.min_lengte_kistdam)
            and not math.isnan(self.max_lengte_kistdam)
        )


class SurroundingsSettings(KoswatConfigProtocol):
    surroundings_database: Path  # Directory
    constructieafstand: float
    constructieovergang: float
    buitendijks: bool
    bebouwing: bool
    spoorwegen: bool
    water: bool

    def __init__(self) -> None:
        self.surroundings_database = None
        self.constructieafstand = math.nan
        self.constructieovergang = math.nan
        self.buitendijks = None
        self.bebouwing = None
        self.spoorwegen = None
        self.water = None

    def is_valid(self) -> bool:
        assert (
            self.surroundings_database is not None
            and not math.isnan(self.constructieafstand)
            and not math.isnan(self.constructieovergang)
            and self.buitendijks is not None
            and self.bebouwing is not None
            and self.spoorwegen is not None
            and self.water is not None
        )


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

    def __init__(self) -> None:
        self.infrastructuur = None
        self.opslagfactor_wegen = None
        self.infrakosten_0dh = None
        self.buffer_buitendijks = math.nan
        self.wegen_klasse2_breedte = math.nan
        self.wegen_klasse24_breedte = math.nan
        self.wegen_klasse47_breedte = math.nan
        self.wegen_klasse7_breedte = math.nan
        self.wegen_onbekend_breedte = math.nan

    def is_valid(self) -> bool:
        return (
            self.infrastructuur is not None
            and self.opslagfactor_wegen is not None
            and self.infrakosten_0dh is not None
            and not math.isnan(self.buffer_buitendijks)
            and not math.isnan(self.wegen_klasse2_breedte)
            and not math.isnan(self.wegen_klasse24_breedte)
            and not math.isnan(self.wegen_klasse47_breedte)
            and not math.isnan(self.wegen_klasse7_breedte)
            and not math.isnan(self.wegen_onbekend_breedte)
        )
