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

from __future__ import annotations

import math

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)


class LayerCostReport(CostReportProtocol):
    layer: ReinforcementLayerProtocol | None
    total_cost: float
    total_cost_with_surtax: float

    def __init__(self) -> None:
        self.layer = None
        self.total_cost = math.nan
        self.total_cost_with_surtax = math.nan

    @property
    def material(self) -> str:
        if not self.layer or not self.layer.material_type:
            return ""
        return self.layer.material_type.name
