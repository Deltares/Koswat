from dataclasses import dataclass

from shapely import LineString

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class ClusterShpFom:
    locations: list[StrategyLocationReinforcement]
    reinforced_profile: ReinforcementProfileProtocol

    @property
    def old_profile_width(self) -> float:
        """
        The original polderside width.
        """
        return self.reinforced_profile.old_profile.profile_width

    @property
    def new_profile_width(self) -> float:
        """
        The new polderside width.
        """
        return self.reinforced_profile.profile_width

    @property
    def base_geometry(self) -> LineString:
        """
        The resulting geometry of all `locations` excluding the
        profile's width.

        Returns:
            LineString: Geometry representing the cluster coordinates.
        """
        return LineString([_l.location.location for _l in self.locations])

    def get_buffered_geometry(self, width: float) -> LineString:
        """
        The `base_geometry` with an applied buffer (`width`) that
        represents the polderside's width.

        Args:
            width (float): Profile's polderside width.

        Returns:
            LineString: Resulting `base_geometry` with a buffer.
        """
        return self.base_geometry.buffer(-width, cap_style=2, single_sided=True)
