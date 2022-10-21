from typing import Type

from koswat.calculations.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfile,
)
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfile,
)
from koswat.cost_report.layer.layer_cost_report_builder_protocol import (
    LayerCostReportBuilderProtocol,
)
from koswat.cost_report.layer.outside_slope_weakening_layer_cost_report_builder import (
    OustideSlopeWeakeningLayerCostReportBuilder,
)
from koswat.cost_report.layer.standard_layer_cost_reinforcement_builder import (
    StandardLayerCostReportBuilder,
)


class LayerCostReportBuilderFactory:
    @staticmethod
    def get_builder(
        reinforcement_type: Type[ReinforcementProfileProtocol],
    ) -> Type[LayerCostReportBuilderProtocol]:

        if issubclass(reinforcement_type, OutsideSlopeReinforcementProfile):
            return OustideSlopeWeakeningLayerCostReportBuilder
        elif issubclass(reinforcement_type, StandardReinforcementProfile):
            return StandardLayerCostReportBuilder
        raise NotImplementedError(
            "No layer cost report builder available for {}".format(reinforcement_type)
        )
