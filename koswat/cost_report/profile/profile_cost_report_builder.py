"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from dataclasses import dataclass

from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.cost_report.profile.layer_cost_report import LayerCostReport
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.profile.quantity_cost_parameters import QuantityCostParameters
from koswat.cost_report.profile.quantity_cost_parameters_builder import (
    QuantityCostParametersBuilder,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class ProfileCostReportBuilder(BuilderProtocol):
    reinforced_profile: ReinforcementProfileProtocol = None
    koswat_costs_settings: KoswatCostsSettings = None

    def _get_layers_report(
        self, cost_parameters: QuantityCostParameters
    ) -> list[LayerCostReport]:
        _reports = []
        for _layer in self.reinforced_profile.layers_wrapper.layers:
            _lcr = LayerCostReport()
            _reports.append(_lcr)
            _lcr.layer = _layer
            (
                _lcr.total_cost,
                _lcr.total_cost_with_surtax,
            ) = cost_parameters.get_material_total_quantity_parameters(
                _layer.material_type
            )
        return _reports

    def build(self) -> ProfileCostReport:
        _report = ProfileCostReport()
        _qcp_builder = QuantityCostParametersBuilder()
        _qcp_builder.reinforced_profile = self.reinforced_profile
        _qcp_builder.koswat_costs_settings = self.koswat_costs_settings
        _report.quantity_cost_parameters = _qcp_builder.build()
        _report.reinforced_profile = self.reinforced_profile
        _report.layer_cost_reports = self._get_layers_report(
            _report.quantity_cost_parameters
        )
        return _report
