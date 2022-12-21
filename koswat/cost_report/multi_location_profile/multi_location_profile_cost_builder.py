from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.protocols import ReinforcementProfileProtocol
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report_builder import (
    ProfileCostReportBuilder,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


class MultiLocationProfileCostReportBuilder(BuilderProtocol):
    surroundings: SurroundingsWrapper
    reinforced_profile: ReinforcementProfileProtocol

    def __init__(self) -> None:
        self.surroundings = None
        self.reinforced_profile = None

    def build(self) -> MultiLocationProfileCostReport:
        _multiple_location_cost_report = MultiLocationProfileCostReport()
        _multiple_location_cost_report.locations = (
            self.surroundings.get_locations_after_distance(
                self.reinforced_profile.profile_width
            )
        )
        _profile_cost_report_builder = ProfileCostReportBuilder()
        _profile_cost_report_builder.reinforced_profile = self.reinforced_profile
        _multiple_location_cost_report.profile_cost_report = (
            _profile_cost_report_builder.build()
        )
        return _multiple_location_cost_report
