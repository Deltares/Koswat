from typing import Type

from koswat.calculations.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfileProtocol,
)
from koswat.calculations.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfileProtocol,
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
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


class LayerCostReportBuilderFactory:
    @staticmethod
    def get_builder(
        koswat_profile: KoswatProfileProtocol,
    ) -> Type[LayerCostReportBuilderProtocol]:
        _builders_dict = {
            OutsideSlopeReinforcementProfileProtocol: OustideSlopeWeakeningLayerCostReportBuilder,
            StandardReinforcementProfileProtocol: StandardLayerCostReportBuilder,
        }
        _builder_type = next(
            (
                _type_build
                for _type_proto, _type_build in _builders_dict.items()
                if isinstance(koswat_profile, _type_proto)
            ),
            None,
        )
        if not _builder_type:
            raise NotImplementedError(
                "No layer cost report builder available for {}".format(koswat_profile)
            )
        return _builder_type
