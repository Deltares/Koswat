from typing import Type

from koswat.calculations import (
    OutsideSlopeReinforcementProfile,
    ReinforcementProfileProtocol,
    StandardReinforcementProfile,
)
from koswat.cost_report.profile.outside_slope_profile_cost_report_builder import (
    OutsideSlopeProfileCostReportBuilder,
)
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.cost_report.profile.standard_profile_cost_report_builder import (
    StandardProfileCostReportBuilder,
)


class ProfileCostReportBuilderFactory:
    @staticmethod
    def get_builder(
        reinforcement_type: Type[ReinforcementProfileProtocol],
    ) -> Type[ProfileCostReportBuilderProtocol]:

        if issubclass(reinforcement_type, OutsideSlopeReinforcementProfile):
            return OutsideSlopeProfileCostReportBuilder
        elif issubclass(reinforcement_type, StandardReinforcementProfile):
            return StandardProfileCostReportBuilder
        raise NotImplementedError(
            "No profile cost report builder available for {}".format(reinforcement_type)
        )
