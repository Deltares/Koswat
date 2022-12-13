from __future__ import annotations

import abc
from configparser import ConfigParser
from pathlib import Path
from typing import List, Optional

import koswat.configuration.io.converters.koswat_analysis_converter as AnalysisConverter
from koswat.configuration.io.converters.koswat_surroundings_converter import (
    from_surroundings_csv_dir_to_fom as as_surroundings_fom,
)
from koswat.configuration.io.csv.koswat_input_profiles_csv_fom import (
    KoswatInputProfilesCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.configuration.io.ini.koswat_costs_ini_fom import KoswatCostsIniFom
from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
)
from koswat.configuration.io.txt.koswat_dike_selection_txt_fom import (
    KoswatDikeSelectionTxtFom,
)
from koswat.configuration.models.koswat_general_settings import (
    InfraCostsEnum,
    StorageFactorEnum,
)
from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class AnalysisSectionFom(KoswatIniFomProtocol):
    dike_selection_txt_fom: KoswatDikeSelectionTxtFom
    dike_section_location_fom: Path  # shp file
    input_profiles_csv_fom: KoswatInputProfilesCsvFom
    scenarios_ini_fom: KoswatSectionScenariosIniFom
    costs_ini_fom: KoswatCostsIniFom
    analysis_output_dir: Path  # output folder
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
        _section.dike_selection_txt_fom = AnalysisConverter.dike_selection_file_to_fom(
            Path(ini_config["dijksecties_selectie"])
        )
        _section.dike_section_location_fom = AnalysisConverter.dike_sections_location_file_to_fom(Path(ini_config["dijksectie_ligging"]))
        _section.input_profiles_csv_fom = (
            AnalysisConverter.dike_input_profiles_file_to_fom(
                Path(ini_config["dijksectie_invoer"])
            )
        )
        _section.scenarios_ini_fom = (
            AnalysisConverter.scenarios_dir_to_koswat_scenario_list(
                Path(ini_config["scenario_invoer"])
            )
        )
        _section.costs_ini_fom = AnalysisConverter.dike_costs_file_to_fom(
            Path(ini_config["eenheidsprijzen"])
        )
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


class SoilReinforcementSectionFom(ReinforcementProfileSectionFomBase):
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


class PipingwallReinforcementSectionFom(ReinforcementProfileSectionFomBase):
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


class StabilitywallReinforcementSectionFom(ReinforcementProfileSectionFomBase):
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


class CofferdamReinforcementSectionFom(ReinforcementProfileSectionFomBase):
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
    surroundings_database: List[KoswatSurroundingsCsvFom]
    constructieafstand: float
    constructieovergang: float
    buitendijks: bool
    bebouwing: bool
    spoorwegen: bool
    water: bool

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.surroundings_database = as_surroundings_fom(
            Path(ini_config["omgevingsdatabases"])
        )
        _section.constructieafstand = ini_config.getfloat("constructieafstand")
        _section.constructieovergang = ini_config.getfloat("constructieovergang")
        _section.buitendijks = ini_config.getboolean("buitendijks")
        _section.bebouwing = ini_config.getboolean("bebouwing")
        _section.spoorwegen = ini_config.getboolean("spoorwegen")
        _section.water = ini_config.getboolean("water")
        return _section


class InfrastructureSectionFom(KoswatIniFomProtocol):
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
    grondmaatregel_section: SoilReinforcementSectionFom
    kwelscherm_section: PipingwallReinforcementSectionFom
    stabiliteitswand_section: StabilitywallReinforcementSectionFom
    kistdam_section: CofferdamReinforcementSectionFom
    surroundings_section: SurroundingsSectionFom
    infrastructuur_section: InfrastructureSectionFom

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _general_ini = cls()

        _general_ini.analyse_section = AnalysisSectionFom.from_config(
            ini_config["Analyse"]
        )
        _general_ini.dijkprofiel_section = DikeProfileSectionFom.from_config(
            ini_config["Dijkprofiel"]
        )
        _general_ini.grondmaatregel_section = SoilReinforcementSectionFom.from_config(
            ini_config["Grondmaatregel"]
        )
        _general_ini.kwelscherm_section = PipingwallReinforcementSectionFom.from_config(
            ini_config["Kwelscherm"]
        )
        _general_ini.stabiliteitswand_section = (
            StabilitywallReinforcementSectionFom.from_config(
                ini_config["Stabiliteitswand"]
            )
        )
        _general_ini.kistdam_section = CofferdamReinforcementSectionFom.from_config(
            ini_config["Kistdam"]
        )
        _general_ini.surroundings_section = SurroundingsSectionFom.from_config(
            ini_config["Omgeving"]
        )
        _general_ini.infrastructuur_section = InfrastructureSectionFom.from_config(
            ini_config["Infrastructuur"]
        )
        return _general_ini
