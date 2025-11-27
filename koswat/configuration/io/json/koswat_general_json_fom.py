from dataclasses import dataclass
from pathlib import Path
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
from koswat.core.io.json.koswat_json_fom import KoswatJsonFom
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
    def from_file(cls, file_path: str) -> "KoswatGeneralJsonFom":
        pass

    @classmethod
    def from_json(cls, koswat_config_fom: KoswatJsonFom) -> "KoswatGeneralJsonFom":
        """
        Creates an instance of `KoswatGeneralJsonFom` from a general configuration dictionary.

        Args:
            koswat_config_fom (KoswatJsonFom): Input configuration.

        Returns:
            KoswatGeneralJsonFom: Created object with parsed config settings.
        """
        json_config = koswat_config_fom.content
        return cls(
            analysis_section=AnalysisSectionFom.from_config(json_config["analyse"], koswat_config_fom.file_path.parent),
            dike_profile_section=DikeProfileSectionFom.from_config(
                json_config["dijkprofiel"], set_defaults=True
            ),
            soil_measure_section=SoilReinforcementSectionFom.from_config(
                json_config["grondmaatregel"], set_defaults=True
            ),
            vps_section=VPSReinforcementSectionFom.from_config(
                json_config["verticalepipingoplossing"], set_defaults=True
            ),
            piping_wall_section=(
                PipingWallReinforcementSectionFom.from_config(
                    json_config["kwelscherm"], set_defaults=True
                )
            ),
            stability_wall_section=(
                StabilitywallReinforcementSectionFom.from_config(
                    json_config["stabiliteitswand"], set_defaults=True
                )
            ),
            cofferdam_section=CofferdamReinforcementSectionFom.from_config(
                dict(json_config["kistdam"]), set_defaults=True
            ),
            surroundings_section=SurroundingsSectionFom.from_config(
                json_config["omgeving"]
            ),
            infrastructuur_section=InfrastructureSectionFom.from_config(
                json_config["infrastructuur"]
            ),
        )
