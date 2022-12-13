import logging
from pathlib import Path
from typing import List

from koswat.configuration.models.koswat_general_settings import KoswatGeneralSettings
from koswat.configuration.models.koswat_scenario import KoswatScenario
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.dike.surroundings.wrapper.surroundings_wrapper_builder import (
    SurroundingsWrapperBuilder,
)


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
        _sections = set(map(lambda x: x.scenario_section, _run_config.scenarios))
        _surroundings_dict = dict()
        # This should be happening at the import time.
        for _section_name in _sections:
            _surroundings_csv = (
                koswat_settings.surroundings_settings.surroundings_database
                / _section_name
                / f"T_{_section_name}_bebouwing_binnendijks.csv"
            )
            if not _surroundings_csv.is_file():
                logging.error(
                    "Surroundings database file not found for traject {}".format(
                        _section_name
                    )
                )
            _surroundings_dict[_section_name] = SurroundingsWrapperBuilder.from_files(
                dict(
                    csv_file=_surroundings_csv,
                    shp_file=koswat_settings.analysis_settings.dike_section_traject_shp_file,
                )
            ).build()


    def run(self) -> None:
        logging.info("Initializing run for all cases.")

        logging.info("Finalized run for all cases.")
