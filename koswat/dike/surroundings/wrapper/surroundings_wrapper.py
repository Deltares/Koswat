from dataclasses import dataclass, field

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)


@dataclass
class SurroundingsWrapper:
    dike_section: str = ""
    traject: str = ""
    subtraject: str = ""

    obstacle_surroundings_wrapper: ObstacleSurroundingsWrapper = field(
        default_factory=ObstacleSurroundingsWrapper
    )
    infrastructure_surroundings_wrapper: InfrastructureSurroundingsWrapper = field(
        default_factory=InfrastructureSurroundingsWrapper
    )

    def get_locations_at_safe_distance(
        self, distance: float
    ) -> list[PointSurroundings]:
        """
        Gets all locations which are safe from obstacle surroundings in a radius of `distance`.

        Args:
            distance (float): Radius from each point that should be free of surroundings.

        Returns:
            List[PointSurroundings]: List of safe locations (points with surroundings).
        """
        return self.obstacle_surroundings_wrapper.get_locations_at_safe_distance(
            distance
        )
