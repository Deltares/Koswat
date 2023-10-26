from dataclasses import dataclass

from koswat.cost_report.summary.koswat_summary_location_matrix import KoswatSummaryLocationMatrix


@dataclass
class StrategyInput:
    locations_matrix: KoswatSummaryLocationMatrix
    structure_buffer: float
    min_space_between_structures: float
