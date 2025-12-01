"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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

from __future__ import annotations

import math
from dataclasses import dataclass, field

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.profile.layer_cost_report import LayerCostReport
from koswat.cost_report.profile.quantity_cost_parameters import QuantityCostParameters
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class ProfileCostReport(CostReportProtocol):
    reinforced_profile: ReinforcementProfileProtocol = None
    quantity_cost_parameters: QuantityCostParameters = field(
        default_factory=QuantityCostParameters
    )
    layer_cost_reports: list[LayerCostReport] = field(default_factory=lambda: [])

    @property
    def total_cost(self) -> float:
        if not self.quantity_cost_parameters:
            return math.nan
        return sum(
            qcp.total_cost for qcp in self.quantity_cost_parameters.get_parameters()
        )

    @property
    def total_cost_with_surtax(self) -> float:
        if not self.quantity_cost_parameters:
            return math.nan
        return sum(
            qcp.total_cost_with_surtax
            for qcp in self.quantity_cost_parameters.get_parameters()
        )
