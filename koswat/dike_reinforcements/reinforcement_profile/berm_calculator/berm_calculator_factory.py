from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator import (
    BermCalculatorProtocol,
    DefaultBermCalculator,
    KeepBermCalculator,
    NoBermCalculator,
    PipingBermCalculator,
    StabilityBermCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculated_factors import (
    BermCalculatedFactors,
)


class BermCalculatorFactory:
    """
    Factory to create the correct berm calculator based on the caluclated factors.
    """

    @staticmethod
    def get_berm_calculator(
        reinforcement_type: InputProfileEnum, calculated_factors: BermCalculatedFactors
    ) -> BermCalculatorProtocol:
        """
        Get the correct berm calculator based on the profile type.

        Args:
            profile_type (InputProfileEnum): The type of profile.
            calculated_factors (BermCalculatedFactors): The calculated factors.

        Returns:
            BermCalculatorProtocol: The correct berm calculator.
        """

        if reinforcement_type == InputProfileEnum.COFFERDAM:
            return BermCalculatorFactory._get_keep_berm_calculator(
                calculated_factors, reinforcement_type
            )

        if reinforcement_type == InputProfileEnum.STABILITY_WALL:
            return BermCalculatorFactory._get_stability_wall_berm_calculator(
                calculated_factors, reinforcement_type
            )

        if calculated_factors.get_dikebase_piping_new(reinforcement_type) > max(
            calculated_factors.dikebase_height_new,
            calculated_factors.dikebase_stability_new,
        ):
            return BermCalculatorFactory._get_piping_berm_calculator(
                calculated_factors, reinforcement_type
            )

        if (
            calculated_factors.dikebase_stability_new
            > calculated_factors.dikebase_height_new
        ):
            if calculated_factors.berm_old_is_stability:
                return BermCalculatorFactory._get_stability_berm_calculator(
                    calculated_factors, reinforcement_type
                )
            return BermCalculatorFactory._get_no_berm_calculator(
                calculated_factors, reinforcement_type
            )

        return BermCalculatorFactory._get_default_berm_calculator(
            calculated_factors, reinforcement_type
        )

    @staticmethod
    def _get_stability_wall_berm_calculator(
        calculated_factors: BermCalculatedFactors,
        reinforcement_type: InputProfileEnum,
    ) -> BermCalculatorProtocol:
        # The stability wall has different logic for the berm calculation
        if (
            max(
                calculated_factors.dikebase_height_new,
                calculated_factors.dikebase_stability_new,
            )
            > calculated_factors.dikebase_piping_old
        ):
            return BermCalculatorFactory._get_no_berm_calculator(
                calculated_factors, reinforcement_type
            )
        if (
            max(
                calculated_factors.dikebase_height_new,
                calculated_factors.dikebase_stability_new,
            )
            < calculated_factors.dikebase_piping_old
        ):
            return BermCalculatorFactory._get_piping_berm_calculator(
                calculated_factors, reinforcement_type
            )
        if (
            calculated_factors.dikebase_stability_new
            > calculated_factors.dikebase_height_new
        ):
            if calculated_factors.berm_old_is_stability:
                return BermCalculatorFactory._get_stability_berm_calculator(
                    calculated_factors, reinforcement_type
                )
            return BermCalculatorFactory._get_no_berm_calculator(
                calculated_factors, reinforcement_type
            )
        return BermCalculatorFactory._get_default_berm_calculator(
            calculated_factors, reinforcement_type
        )

    @staticmethod
    def _get_keep_berm_calculator(
        calculated_factors: BermCalculatedFactors,
        reinforcement_type: InputProfileEnum,
    ) -> BermCalculatorProtocol:
        return KeepBermCalculator(
            scenario=calculated_factors.scenario,
            dikebase_piping_old=calculated_factors.dikebase_piping_old,
            dikebase_piping_new=calculated_factors.get_dikebase_piping_new(
                reinforcement_type
            ),
            dike_height_new=calculated_factors.dike_height_new,
        )

    @staticmethod
    def _get_piping_berm_calculator(
        calculated_factors: BermCalculatedFactors,
        reinforcement_type: InputProfileEnum,
    ) -> BermCalculatorProtocol:
        return PipingBermCalculator(
            scenario=calculated_factors.scenario,
            reinforcement_settings=calculated_factors.reinforcement_settings,
            dikebase_piping_old=calculated_factors.dikebase_piping_old,
            dikebase_piping_new=calculated_factors.get_dikebase_piping_new(
                reinforcement_type
            ),
            dikebase_height_new=calculated_factors.dikebase_height_new,
            dikebase_stability_new=calculated_factors.dikebase_stability_new,
            dike_height_new=calculated_factors.dike_height_new,
        )

    @staticmethod
    def _get_stability_berm_calculator(
        calculated_factors: BermCalculatedFactors,
        reinforcement_type: InputProfileEnum,
    ) -> BermCalculatorProtocol:
        return StabilityBermCalculator(
            scenario=calculated_factors.scenario,
            reinforcement_settings=calculated_factors.reinforcement_settings,
            dikebase_piping_old=calculated_factors.dikebase_piping_old,
            dikebase_piping_new=calculated_factors.get_dikebase_piping_new(
                reinforcement_type
            ),
            dikebase_height_new=calculated_factors.dikebase_height_new,
            dikebase_stability_new=calculated_factors.dikebase_stability_new,
            dike_height_new=calculated_factors.dike_height_new,
            berm_factor_old=calculated_factors.berm_factor_old,
        )

    @staticmethod
    def _get_no_berm_calculator(
        calculated_factors: BermCalculatedFactors,
        reinforcement_type: InputProfileEnum,
    ) -> BermCalculatorProtocol:
        return NoBermCalculator(
            scenario=calculated_factors.scenario,
            reinforcement_settings=calculated_factors.reinforcement_settings,
            dikebase_piping_old=calculated_factors.dikebase_piping_old,
            dikebase_piping_new=calculated_factors.get_dikebase_piping_new(
                reinforcement_type
            ),
            dikebase_height_new=calculated_factors.dikebase_height_new,
            dikebase_stability_new=calculated_factors.dikebase_stability_new,
            dike_height_new=calculated_factors.dike_height_new,
            reinforcement_type=reinforcement_type,
        )

    @staticmethod
    def _get_default_berm_calculator(
        calculated_factors: BermCalculatedFactors,
        reinforcement_type: InputProfileEnum,
    ) -> BermCalculatorProtocol:
        return DefaultBermCalculator(
            dikebase_piping_old=calculated_factors.dikebase_piping_old,
            dikebase_piping_new=calculated_factors.get_dikebase_piping_new(
                reinforcement_type
            ),
            dike_height_new=calculated_factors.dike_height_new,
        )
