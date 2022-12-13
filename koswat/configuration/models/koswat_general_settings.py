from __future__ import annotations

import abc
import enum
import math
from pathlib import Path
from typing import List, Optional

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.models.koswat_costs import KoswatCosts
from koswat.configuration.models.koswat_dike_selection import KoswatDikeSelection
from koswat.configuration.models.koswat_scenario import KoswatScenario
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


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
    dike_section_traject_shp_file: Path  # shp file
    dike_sections_input_profile: List[KoswatInputProfileBase]
    include_taxes: bool

    def __init__(self) -> None:
        self.dike_selection = None
        self.scenarios = None
        self.costs = None
        self.analysis_output = None
        self.dike_section_traject_shp_file = None
        self.dike_sections_input_profile = None
        self.include_taxes = True  # Default value.

    def is_valid(self) -> bool:
        return (
            self.dike_selection.is_valid()
            and all(_s.is_valid() for _s in self.scenarios)
            and self.costs.is_valid()
            and self.analysis_output is not None
            and self.dike_section_traject_shp_file.is_file()
            and any(self.dike_sections_input_profile)
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
                dict(
                    material=KoswatMaterialType.GRASS, depth=self.thickness_grass_layer
                ),
                dict(material=KoswatMaterialType.CLAY, depth=self.thickness_clay_layer),
            ],
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
        _reinforcent_base_validation = super(SoilSettings, self).is_valid()
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
        _reinforcent_base_validation = super(PipingwallSettings, self).is_valid()
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
        _reinforcent_base_validation = super(StabilitywallSettings, self).is_valid()
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
        _reinforcent_base_validation = super(CofferdamSettings, self).is_valid()
        return (
            _reinforcent_base_validation
            and not math.isnan(self.min_lengte_kistdam)
            and not math.isnan(self.max_lengte_kistdam)
        )


class SurroundingsSettings(KoswatConfigProtocol):
    surroundings_database: Optional[List[KoswatSurroundingsCsvFom]]
    constructieafstand: float
    constructieovergang: float
    buitendijks: bool
    bebouwing: bool
    spoorwegen: bool
    water: bool

    def __init__(self) -> None:
        self.surroundings_database = []
        self.constructieafstand = math.nan
        self.constructieovergang = math.nan
        self.buitendijks = None
        self.bebouwing = None
        self.spoorwegen = None
        self.water = None

    def is_valid(self) -> bool:
        return (
            not math.isnan(self.constructieafstand)
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


class KoswatGeneralSettings(KoswatConfigProtocol):
    analysis_settings: AnalysisSettings
    dike_profile_settings: DikeProfileSettings
    soil_settings: SoilSettings
    pipingwall_settings: PipingwallSettings
    stabilitywall_settings: StabilitywallSettings
    cofferdam_settings: CofferdamSettings
    surroundings_settings: SurroundingsSettings
    infrastructure_settings: InfrastructuurSettings

    def __init__(self) -> None:
        self.analysis_settings = None
        self.dike_profile_settings = None
        self.soil_settings = None
        self.pipingwall_settings = None
        self.stabilitywall_settings = None
        self.cofferdam_settings = None
        self.surroundings_settings = None
        self.infrastructure_settings = None

    def is_valid(self) -> bool:
        def valid_prop_config(config_property: KoswatConfigProtocol) -> bool:
            return config_property is not None and config_property.is_valid()

        return all(valid_prop_config(_config) for _config in self.__dict__.values())
