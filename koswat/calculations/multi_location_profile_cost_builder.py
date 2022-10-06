from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.profile_cost_builder import ProfileCostBuilder
from koswat.koswat_report import MultiLocationProfileCostReport
from koswat.profiles.koswat_profile import KoswatProfileBase
from koswat.surroundings.koswat_surroundings import KoswatSurroundings


class MultiLocationProfileCostBuilder(BuilderProtocol):
    surroundings: KoswatSurroundings
    base_profile: KoswatProfileBase
    calc_profile: KoswatProfileBase

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.calc_profile = None

    def _get_profile_cost_builder(self) -> ProfileCostBuilder:
        _profile_cost_builder = ProfileCostBuilder()
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
