from dataclasses import dataclass

from koswat.cost_report.summary import koswat_summary_location_matrix_builder


@dataclass
class StrategyInput:
    locations_matrix: koswat_summary_location_matrix_builder
    structure_buffer: float
    min_space_between_structures: float
