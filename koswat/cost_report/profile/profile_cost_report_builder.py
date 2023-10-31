from typing import List

from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.cost_report.profile.layer_cost_report import LayerCostReport
from koswat.cost_report.profile.profile_cost_report import (
    LayerCostReport,
    ProfileCostReport,
)
from koswat.cost_report.profile.volume_cost_parameters import VolumeCostParameters
from koswat.cost_report.profile.volume_cost_parameters_builder import (
    VolumeCostParametersBuilder,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class ProfileCostReportBuilder(BuilderProtocol):
    reinforced_profile: ReinforcementProfileProtocol
    koswat_costs_settings: KoswatCostsSettings

    def __init__(self) -> None:
        self.reinforced_profile = None
        self.koswat_costs_settings = None

    def _get_layers_report(
        self, cost_parameters: VolumeCostParameters
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
        _vcp_builder = VolumeCostParametersBuilder()
        _vcp_builder.reinforced_profile = self.reinforced_profile
        _vcp_builder.koswat_costs_settings = self.koswat_costs_settings
        _report.volume_cost_parameters = _vcp_builder.build()
        _report.reinforced_profile = self.reinforced_profile
        _report.layer_cost_reports = self._get_layers_report(
            _report.volume_cost_parameters
        )
        return _report
