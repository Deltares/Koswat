from typing import List

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.cost_report.profile.layer_cost_report import LayerCostReport
from koswat.cost_report.profile.profile_cost_report import (
    LayerCostReport,
    ProfileCostReport,
)
from koswat.cost_report.profile.volume_cost_parameters import VolumeCostParameters


class ProfileCostReportBuilder(BuilderProtocol):
    reinforced_profile: ReinforcementProfileProtocol

    def _get_layers_report(
        self, cost_parameters: List[VolumeCostParameters]
    ) -> List[LayerCostReport]:
        _reports = []
        for _layer in self.reinforced_profile.layers_wrapper.layers:
            _lcr = LayerCostReport()
            _reports.append(_lcr)
            _lcr.layer = _layer
            (
                _lcr.total_volume,
                _lcr.total_cost,
            ) = cost_parameters.get_material_total_volume_parameters(
                _layer.material_type
            )
        return _reports

    def build(self) -> ProfileCostReport:
        _report = ProfileCostReport()
        _report.volume_cost_parameters = VolumeCostParameters.from_reinforced_profile(
            self.reinforced_profile
        )
        _report.reinforced_profile = self.reinforced_profile
        _report.layer_cost_reports = self._get_layers_report(
            _report.volume_cost_parameters
        )

        return _report
