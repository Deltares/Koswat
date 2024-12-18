from typing import Protocol, runtime_checkable

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


@runtime_checkable
class BermCalculatorProtocol(Protocol):
    """
    Protocol for calculating the berm width, height and slope for the polderside or waterside of the dike.
    The attributes defined here are required as they are requested by some profile calculations.
    """

    dikebase_piping_old: float
    dikebase_piping_new: float
    dike_height_new: float

    def calculate(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
    ) -> tuple[float, float, float]:
        """
        Calculate the berm width, height and slope for the polderside or waterside of the dike.

        Args:
            base_data (KoswatInputProfileProtocol): The input profile data.
            reinforced_data (KoswatInputProfileProtocol): The reinforced profile data.

        Returns:
            tuple[float, float, float]: The berm width, height and slope.
        """
