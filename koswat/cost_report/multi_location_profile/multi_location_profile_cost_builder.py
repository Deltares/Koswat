from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report_builder import (
    ProfileCostReportBuilder,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class MultiLocationProfileCostReportBuilder(BuilderProtocol):
    surroundings: SurroundingsWrapper
    reinforced_profile: ReinforcementProfileProtocol
    koswat_costs_settings: KoswatCostsSettings

    def __init__(self) -> None:
        self.surroundings = None
        self.reinforced_profile = None
        self.koswat_costs_settings = None

    def build(self) -> MultiLocationProfileCostReport:

        # Profile cost report builder
        _profile_cost_report_builder = ProfileCostReportBuilder(
            reinforced_profile=self.reinforced_profile,
            koswat_costs_settings=self.koswat_costs_settings,
        )

        # Multi-location profile cost report
        return MultiLocationProfileCostReport(
            obstacle_locations=self.surroundings.get_locations_at_safe_distance(
                self.reinforced_profile.profile_width
            ),
            profile_cost_report=_profile_cost_report_builder.build(),
            infrastructure_matrix=self.surroundings.infrastructure_surroundings_wrapper,
        )
