from koswat.builder_protocol import BuilderProtocol
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report_builder_factory import (
    ProfileCostReportBuilderFactory,
)
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


class MultiLocationProfileCostReportBuilder(BuilderProtocol):
    surroundings: SurroundingsWrapper
    base_profile: KoswatProfileBase
    calc_profile: KoswatProfileBase

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.calc_profile = None

    def _get_profile_cost_builder(self) -> ProfileCostReportBuilderProtocol:
        _profile_cost_builder = ProfileCostReportBuilderFactory.get_builder(
            type(self.calc_profile)
        )
        _profile_cost_builder.base_profile = self.base_profile
        _profile_cost_builder.calculated_profile = self.calc_profile
        return _profile_cost_builder

    def build(self) -> MultiLocationProfileCostReport:
        _multiple_location_cost_report = MultiLocationProfileCostReport()
        _multiple_location_cost_report.locations = (
            self.surroundings.buldings_polderside.get_locations_after_distance(
                self.calc_profile.profile_width
            )
        )
        _multiple_location_cost_report.profile_cost_report = (
            self._get_profile_cost_builder().build()
        )
        return _multiple_location_cost_report
