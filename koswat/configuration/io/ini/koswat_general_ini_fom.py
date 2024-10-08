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
    min_bermhoogte: float
    max_bermhoogte_factor: float
    factor_toename_bermhoogte: float
    land_purchase_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_bermhoogte = ini_config.getfloat("min_bermhoogte")
        _section.max_bermhoogte_factor = ini_config.getfloat("max_bermhoogte_factor")
        _section.factor_toename_bermhoogte = ini_config.getfloat(
            "factor_toename_bermhoogte"
        )
        _section.land_purchase_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_grondaankoop", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        return _section


class VPSReinforcementSectionFom(ReinforcementProfileSectionFomBase):
    binnen_berm_breedte_vps: float
    constructive_surtax_factor: float
    land_purchase_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.binnen_berm_breedte_vps = ini_config.getfloat(
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
    min_lengte_kwelscherm: float
    overgang_cbwand_damwand: float
    max_lengte_kwelscherm: float
    constructive_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_lengte_kwelscherm = ini_config.getfloat("min_lengte_kwelscherm")
        _section.overgang_cbwand_damwand = ini_config.getfloat(
            "overgang_cbwand_damwand"
        )
        _section.max_lengte_kwelscherm = ini_config.getfloat("max_lengte_kwelscherm")
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
    versteiling_binnentalud: float
    min_lengte_stabiliteitswand: float
    overgang_damwand_diepwand: float
    max_lengte_stabiliteitswand: float
    constructive_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.versteiling_binnentalud = ini_config.getfloat(
            "versteiling_binnentalud"
        )
        _section.min_lengte_stabiliteitswand = ini_config.getfloat(
            "min_lengte_stabiliteitswand"
        )
        _section.overgang_damwand_diepwand = ini_config.getfloat(
            "overgang_damwand_diepwand"
        )
        _section.max_lengte_stabiliteitswand = ini_config.getfloat(
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
    min_lengte_kistdam: float
    max_lengte_kistdam: float
    constructive_surtax_factor: SurtaxFactorEnum

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section._set_properties_from_dict(ini_config)
        _section.min_lengte_kistdam = ini_config.getfloat("min_lengte_kistdam")
        _section.max_lengte_kistdam = ini_config.getfloat("max_lengte_kistdam")
        _section.constructive_surtax_factor = SurtaxFactorEnum[
            ini_config.get(
                "opslagfactor_constructief", SurtaxFactorEnum.NORMAAL.name
            ).upper()
        ]
        return _section


@dataclass
class SurroundingsSectionFom(KoswatIniFomProtocol):
    surroundings_database_dir: Path
    constructieafstand: float
    constructieovergang: float
    buitendijks: bool
    bebouwing: bool
    spoorwegen: bool
    water: bool

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls(
            surroundings_database_dir=Path(ini_config["omgevingsdatabases"]),
            constructieafstand=ini_config.getfloat("constructieafstand"),
            constructieovergang=ini_config.getfloat("constructieovergang"),
            buitendijks=ini_config.getboolean("buitendijks"),
            bebouwing=ini_config.getboolean("bebouwing"),
            spoorwegen=ini_config.getboolean("spoorwegen"),
            water=ini_config.getboolean("water"),
        )
        return _section


@dataclass
class InfrastructureSectionFom(KoswatIniFomProtocol):
    infrastructuur: bool
    opslagfactor_wegen: SurtaxFactorEnum
    infrakosten_0dh: InfraCostsEnum
    buffer_buitendijks: float
    wegen_klasse2_breedte: float
    wegen_klasse24_breedte: float
    wegen_klasse47_breedte: float
    wegen_klasse7_breedte: float
    wegen_onbekend_breedte: float

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        return cls(
            infrastructuur=ini_config.getboolean("infrastructuur"),
            opslagfactor_wegen=SurtaxFactorEnum[
                ini_config["opslagfactor_wegen"].upper()
            ],
            infrakosten_0dh=InfraCostsEnum[ini_config["infrakosten_0dh"].upper()],
            buffer_buitendijks=ini_config.getfloat("buffer_buitendijks"),
            wegen_klasse2_breedte=ini_config.getfloat("wegen_klasse2_breedte"),
            wegen_klasse24_breedte=ini_config.getfloat("wegen_klasse24_breedte"),
            wegen_klasse47_breedte=ini_config.getfloat("wegen_klasse47_breedte"),
            wegen_klasse7_breedte=ini_config.getfloat("wegen_klasse7_breedte"),
            wegen_onbekend_breedte=ini_config.getfloat("wegen_onbekend_breedte"),
        )


class KoswatGeneralIniFom(KoswatIniFomProtocol):
    analyse_section_fom: AnalysisSectionFom
    dike_profile_section_fom: DikeProfileSectionFom
    grondmaatregel_section: SoilReinforcementSectionFom
    vps_section: VPSReinforcementSectionFom
    kwelscherm_section: PipingwallReinforcementSectionFom
    stabiliteitswand_section: StabilitywallReinforcementSectionFom
    kistdam_section: CofferdamReinforcementSectionFom
    surroundings_section: SurroundingsSectionFom
    infrastructuur_section: InfrastructureSectionFom

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _general_ini = cls()

        _general_ini.analyse_section_fom = AnalysisSectionFom.from_config(
            ini_config["Analyse"]
        )
        _general_ini.dike_profile_section_fom = DikeProfileSectionFom.from_config(
            ini_config["Dijkprofiel"]
        )
        _general_ini.grondmaatregel_section = SoilReinforcementSectionFom.from_config(
            ini_config["Grondmaatregel"]
        )
        _general_ini.vps_section = VPSReinforcementSectionFom.from_config(
            ini_config["VerticalePipingOplossing"]
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
