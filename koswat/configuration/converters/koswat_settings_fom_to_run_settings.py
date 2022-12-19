import logging

from koswat.configuration.converters.koswat_settings_fom_converter_base import (
    KoswatSettingsFomConverterBase,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.configuration.settings.koswat_run_settings import (
    KoswatRunScenarioSettings,
    KoswatRunSettings,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike.surroundings.wrapper.surroundings_wrapper_builder import (
    SurroundingsWrapperBuilder,
)


class KoswatSettingsFomToRunSettings(KoswatSettingsFomConverterBase):
    def _get_surroundings_wrapper(
        self,
        trajects_fom: KoswatDikeLocationsShpFom,
        surroundings_fom: KoswatTrajectSurroundingsWrapperCsvFom,
    ) -> SurroundingsWrapper:
        _builder = SurroundingsWrapperBuilder()
        _builder.surroundings_fom = surroundings_fom
        _builder.trajects_fom = trajects_fom
        return _builder.build()

    def convert_settings(self) -> KoswatRunSettings:
        _run_settings = KoswatRunSettings()

        _dike_selected_sections = (
            self.fom_settings.analyse_section_fom.dike_selection_txt_file.dike_sections
        )

        # Define scenarios
        # TODO: Reduce complexity.
        # for _fom_scenario in self.fom_settings.analyse_section_fom.scenarios_ini_file:
        #     if _fom_scenario.scenario_section not in _dike_selected_sections:
        #         logging.error(
        #             "Scenario {} won't be run because section was not selected.".format(
        #                 _fom_scenario.scenario_section
        #             )
        #         )
        #         continue
        #     _scenario_output = _run_settings.output_dir / (
        #         "scenario_" + _fom_scenario.scenario_section
        #     )
        #     for (
        #         _shp_dike_fom
        #     ) in self.fom_settings.analyse_section_fom.dike_section_location_file.get_by_section(
        #         _fom_scenario.scenario_section
        #     ):
        #         _csv_db = self.fom_settings.surroundings_section.surroundings_database.get_wrapper_by_traject(
        #             _shp_dike_fom.record.Traject.replace(
        #                 "-", "_"
        #             )  # We know the csv files are with '-' whilst the shp values are '_'
        #         )
        #         if not _csv_db:
        #             logging.warning(
        #                 "No surroundings found for {}".format(
        #                     _shp_dike_fom.record.Traject
        #                 )
        #             )
        #             # TODO: For now we will skip until clarity on what to do in this case.
        #             continue
        #         _surroundings = self._get_surroundings_wrapper(_shp_dike_fom, _csv_db)
        #         for _sub_scenario in _fom_scenario.section_scenarios:
        #             _sub_output = _scenario_output / _sub_scenario.scenario_name
        #             for _input_profile in _input_profile_cases:
        #                 _run_scenario = KoswatRunScenarioSettings()
        #                 _run_scenario.input_profile_case = _input_profile
        #                 _run_scenario.scenario = self._get_koswat_scenario(
        #                     _sub_scenario, _input_profile
        #                 )
        #                 _run_scenario.surroundings = _surroundings
        #                 _run_scenario.costs = _costs
        #                 _run_scenario.output_dir = (
        #                     _sub_output / _input_profile.input_data.dike_section
        #                 )
        #                 _run_settings.run_scenarios.append(_run_scenario)

        return _run_settings
