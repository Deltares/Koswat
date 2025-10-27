from dataclasses import dataclass, field

from koswat.configuration.io.config_sections import (
    CofferdamReinforcementSectionFom,
    DikeProfileSectionFom,
    PipingwallReinforcementSectionFom,
    SoilReinforcementSectionFom,
    StabilitywallReinforcementSectionFom,
    VPSReinforcementSectionFom,
)
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@dataclass
class KoswatDikeSectionInputJsonFom(FileObjectModelProtocol):
    dike_section: str = ""
    input_profile: DikeProfileSectionFom = field(default_factory=DikeProfileSectionFom)
    soil_measure: SoilReinforcementSectionFom = field(
        default_factory=SoilReinforcementSectionFom
    )
    vps: VPSReinforcementSectionFom = field(default_factory=VPSReinforcementSectionFom)
    piping_wall: PipingwallReinforcementSectionFom = field(
        default_factory=PipingwallReinforcementSectionFom
    )
    stability_wall: StabilitywallReinforcementSectionFom = field(
        default_factory=StabilitywallReinforcementSectionFom
    )
    cofferdam: CofferdamReinforcementSectionFom = field(
        default_factory=CofferdamReinforcementSectionFom
    )

    def is_valid(self) -> bool:
        return self.dike_section != ""
