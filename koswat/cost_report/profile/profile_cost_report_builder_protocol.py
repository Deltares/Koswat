from typing import Protocol

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations import reinforcement_profile_protocol
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


class ProfileCostReportBuilderProtocol(BuilderProtocol, Protocol):
    base_profile: KoswatProfileProtocol
    calculated_profile: reinforcement_profile_protocol

    def build(self) -> ProfileCostReport:
        """
        Generates an instance of a `ProfileCostReport` based on the required properties.

        Returns:
            ProfileCostReport: Instance of a `ProfileCostReport`.
        """
        pass
