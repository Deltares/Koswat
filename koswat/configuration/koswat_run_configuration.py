import logging
from pathlib import Path
from typing import List

from koswat.configuration.settings.koswat_general_settings import KoswatGeneralSettings
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder


class KoswatRunConfiguration:
    input_cases: List[KoswatProfileBase]
    scenarios: List[KoswatScenario]
    surroundings: List[Path]

    @classmethod
    def from_settings(cls, koswat_settings: KoswatGeneralSettings) -> None:
        _run_config = cls()
        if not koswat_settings.is_valid():
            logging.error(
                "Current configuration is not valid. Analysis can't go further."
            )
        _run_config._koswat_settings = koswat_settings

        # Define base profiles
        _run_config.input_cases = []
        for (
            _input_case
        ) in koswat_settings.analysis_settings.dike_sections_input_profile:
            _input_profile = KoswatProfileBuilder.with_data(
                dict(
                    input_profile_data=_input_case,
                    layers_data=koswat_settings.dike_profile_settings.get_material_thickness(),
                    profile_type=KoswatProfileBase,
                )
            )
            _run_config.input_cases.append(_input_profile)

        # Define scenarios
        _run_config.scenarios = koswat_settings.analysis_settings.scenarios

        # Define surroundings
        _run_config.surroundings = list(
            koswat_settings.surroundings_settings.surroundings_database.iterdir()
        )

    def run(self) -> None:
        logging.info("Initializing run for all cases.")

        logging.info("Finalized run for all cases.")
