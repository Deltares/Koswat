from dataclasses import dataclass
from typing import Any

from koswat.configuration.io.config_sections import (
    AnalysisSectionFom,
    CofferdamReinforcementSectionFom,
    DikeProfileSectionFom,
    InfrastructureSectionFom,
    PipingWallReinforcementSectionFom,
    SoilReinforcementSectionFom,
    StabilitywallReinforcementSectionFom,
    SurroundingsSectionFom,
    VPSReinforcementSectionFom,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


@dataclass
class KoswatGeneralJsonFom(KoswatJsonFomProtocol):
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
    def from_config(cls, input_config: dict[str, Any]) -> "KoswatGeneralJsonFom":
        """
        Creates an instance of `KoswatGeneralJsonFom` from a general configuration dictionary.

        Args:
            input_config (dict[str, Any]): Input configuration.

        Returns:
            KoswatGeneralJsonFom: Created object with parsed config settings.
        """
        _general_ini = cls()

        _general_ini.analysis_section = AnalysisSectionFom.from_config(
            input_config["analyse"]
        )
        _general_ini.dike_profile_section = DikeProfileSectionFom.from_config(
            input_config["dijkprofiel"], set_defaults=True
        )
        _general_ini.soil_measure_section = SoilReinforcementSectionFom.from_config(
            input_config["grondmaatregel"], set_defaults=True
        )
        _general_ini.vps_section = VPSReinforcementSectionFom.from_config(
            input_config["verticalePipingOplossing"], set_defaults=True
        )
        _general_ini.piping_wall_section = (
            PipingWallReinforcementSectionFom.from_config(
                input_config["kwelscherm"], set_defaults=True
            )
        )
        _general_ini.stability_wall_section = (
            StabilitywallReinforcementSectionFom.from_config(
                input_config["stabiliteitswand"], set_defaults=True
            )
        )
        _general_ini.cofferdam_section = CofferdamReinforcementSectionFom.from_config(
            dict(input_config["kistdam"]), set_defaults=True
        )
        _general_ini.surroundings_section = SurroundingsSectionFom.from_config(
            input_config["omgeving"]
        )
        _general_ini.infrastructuur_section = InfrastructureSectionFom.from_config(
            input_config["infrastructuur"]
        )
        return _general_ini
