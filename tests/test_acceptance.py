from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable, Iterable, Iterator

import cv2
import numpy as np
import pytest

from koswat.configuration.io.config_sections import (
    InfrastructureSectionFom,
    SurroundingsSectionFom,
)
from koswat.configuration.io.json.koswat_general_json_fom import KoswatGeneralJsonFom
from koswat.configuration.io.koswat_costs_importer import KoswatCostsImporter
from koswat.configuration.io.surroundings_wrapper_collection_importer import (
    SurroundingsWrapperCollectionImporter,
)
from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.costs.construction_costs_settings import (
    ConstructionCostsSettings,
    ConstructionFactors,
)
from koswat.configuration.settings.costs.dike_profile_costs_settings import (
    DikeProfileCostsSettings,
)
from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.configuration.settings.costs.surtax_costs_settings import (
    SurtaxCostsSettings,
)
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.core.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.infrastructure.infrastructure_location_profile_cost_report import (
    InfrastructureLocationProfileCostReport,
)
from koswat.cost_report.io.plots.multi_location_profile_comparison_plot_exporter import (
    MultiLocationProfileComparisonPlotExporter,
)
from koswat.cost_report.io.summary.koswat_summary_exporter import KoswatSummaryExporter
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.summary import KoswatSummary, KoswatSummaryBuilder
from koswat.dike.profile import KoswatProfileBase, KoswatProfileBuilder
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike_reinforcements import ReinforcementProfileBuilderFactory
from koswat.strategies.infra_priority_strategy.infra_priority_strategy import (
    InfraPriorityStrategy,
)
from tests import (
    get_fixturerequest_case_name,
    get_testcase_results_dir,
    test_data,
    test_data_acceptance,
    test_results,
)
from tests.acceptance_scenarios.acceptance_test_scenario_cases import (
    acceptance_test_combinations,
)
from tests.acceptance_scenarios.acceptance_test_scenario_dataclasses import (
    AcceptanceTestScenario,
    AcceptanceTestScenarioCombinations,
)
from tests.acceptance_scenarios.koswat_input_profile_base_cases import InputProfileCases
from tests.acceptance_scenarios.koswat_scenario_test_cases import ScenarioCases
from tests.acceptance_scenarios.layers_cases import LayersCases


class TestAcceptance:
    def test_koswat_package_can_be_imported(self):
        """
        Import test. Not really necessary given the current way we are testing (directly to the cli). But better safe than sorry.
        """

        try:
            import koswat
            import koswat.__main__
        except ImportError as exc_err:
            pytest.fail(f"It was not possible to import required packages {exc_err}")

    @pytest.fixture(name="koswat_acceptance_settings")
    def _get_koswat_acceptance_settings_fixtures(
        self,
    ) -> Iterator[Callable[[], tuple[KoswatGeneralJsonFom, KoswatCostsSettings]]]:
        # Config parser to map the settings to a real case
        _json = KoswatJsonReader().read(
            test_data_acceptance.joinpath("koswat_general.json")
        )
        _koswat_general_settings = KoswatGeneralJsonFom.from_config(_json.content)

        # It is easier returning the costs directly than the FOM,
        # as there's no direct converter from `KoswatCostsIniFom` to `KoswatCosts`
        _costs_importer = KoswatCostsImporter()
        _costs_importer.include_taxes = True
        _koswat_costs = _costs_importer.import_from(
            test_data_acceptance.joinpath("koswat_costs.ini")
        )

        yield lambda: (_koswat_general_settings, _koswat_costs)

    @pytest.fixture(
        name="t_10_3_surroundings_wrapper_fixture",
        params=[(False, False), (False, True), (True, False), (True, True)],
        ids=[
            "Without ANY surrounding",
            "With Infrastructure",
            "With Obstacles",
            "With Infra and Obstacles",
        ],
    )
    def _get_surroundings_wrapper_fixture(
        self,
        koswat_acceptance_settings: Callable[
            [], tuple[KoswatGeneralJsonFom, KoswatCostsSettings]
        ],
        request: pytest.FixtureRequest,
    ) -> Iterable[tuple[SurroundingsWrapper, KoswatCostsSettings, Path]]:
        _traject = "10_3"
        # Shp locations file
        _shp_file = test_data.joinpath(
            "shp_reader",
            "Dijkvak",
            "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp",
        )
        assert _shp_file.is_file()

        # Surroundings directory
        _surroundings_analysis_path = test_data_acceptance.joinpath(
            "surroundings_analysis", _traject
        )
        assert _surroundings_analysis_path.is_dir()

        # Create a dummy dir to avoid importing unnecessary data.
        _dir_name = get_testcase_results_dir(request)
        _temp_dir = test_results.joinpath(_dir_name, _traject)
        if _temp_dir.exists():
            shutil.rmtree(_temp_dir)
        shutil.copytree(_surroundings_analysis_path, _temp_dir)

        # Set surroundings (obstacles / infras)
        _include_obstacles, _include_infras = request.param

        # Generate surroundings section File Object Model.
        _koswat_general_settings, _koswat_costs = koswat_acceptance_settings()
        _surroundings_settings = _koswat_general_settings.surroundings_section
        _surroundings_settings.surroundings_database_dir = _temp_dir.parent
        _surroundings_settings.buildings = _include_obstacles

        # Generate Infrastructures section file model
        _infrastructure_settings = _koswat_general_settings.infrastructuur_section
        _infrastructure_settings.infrastructure = _include_infras

        # Generate wrapper
        _importer = SurroundingsWrapperCollectionImporter(
            infrastructure_section_fom=_infrastructure_settings,
            surroundings_section_fom=_surroundings_settings,
            selected_locations=[],
            traject_loc_shp_file=_shp_file,
        )
        _surroundings_wrapper_list = _importer.build()
        assert any(_surroundings_wrapper_list)

        # Yield result
        yield _surroundings_wrapper_list[0], _koswat_costs, _temp_dir

        if not _include_infras:
            # Do not keep analysis results when no infrastructures are included.
            shutil.rmtree(_temp_dir)

    @pytest.mark.parametrize("input_profile_case", InputProfileCases.cases)
    @pytest.mark.parametrize("scenario_case", ScenarioCases.cases)
    @pytest.mark.parametrize(
        "layers_case",
        LayersCases.cases,
    )
    @pytest.mark.slow
    def test_koswat_run_as_sandbox_with_obstacles_and_infrastructures(
        self,
        input_profile_case,
        scenario_case: KoswatProfileBase,
        layers_case,
        t_10_3_surroundings_wrapper_fixture: tuple[
            SurroundingsWrapper, KoswatCostsSettings, Path
        ],
    ):
        """
        IMPORTANT! When these tests fail in TC they make the build stall
        for a (yet) unknown reason.
        """
        # 1. Define test data.
        (
            _surroundings_wrapper,
            _cost_settings,
            _test_dir,
        ) = t_10_3_surroundings_wrapper_fixture

        assert _test_dir.exists()
        assert isinstance(_surroundings_wrapper, SurroundingsWrapper)

        # Define scenario settings.
        _run_settings = KoswatRunScenarioSettings(
            scenario=scenario_case,
            surroundings=_surroundings_wrapper,
            costs_setting=_cost_settings,
            reinforcement_settings=KoswatReinforcementSettings(),
            input_profile_case=KoswatProfileBuilder.with_data(
                dict(
                    input_profile_data=input_profile_case,
                    layers_data=layers_case,
                    profile_type=KoswatProfileBase,
                )
            ).build(),
        )

        # 2. Run test.
        _summary = KoswatSummaryBuilder(
            run_scenario_settings=_run_settings, strategy_type=InfraPriorityStrategy
        ).build()
        assert isinstance(_summary, KoswatSummary)

        # 3. Verify expectations.
        # TODO: These checks take extremely long time  when infrastructures are present
        assert any(_summary.locations_profile_report_list)

        KoswatSummaryExporter().export(_summary, _test_dir)
        assert _test_dir.joinpath("summary_costs.csv").exists()

        # Validate obstacles.
        if _surroundings_wrapper.obstacle_surroundings_wrapper.buildings.points:
            assert _test_dir.joinpath("summary_locations.csv").exists()

        # Validate infrastructures.
        if (
            not _surroundings_wrapper.infrastructure_surroundings_wrapper.infrastructures_considered
        ):
            return
        assert _test_dir.joinpath("summary_infrastructure_costs.csv").exists()

        def check_valid_infra_reports(
            mlpc_report: MultiLocationProfileCostReport,
        ) -> bool:
            assert isinstance(mlpc_report, MultiLocationProfileCostReport)
            assert any(mlpc_report.infra_multilocation_profile_cost_report)
            assert all(
                isinstance(_infra_report, InfrastructureLocationProfileCostReport)
                for _infra_report in mlpc_report.infra_multilocation_profile_cost_report
            )
            return True

        assert all(
            map(check_valid_infra_reports, _summary.locations_profile_report_list)
        )

    @pytest.mark.parametrize("input_profile_case", InputProfileCases.cases)
    @pytest.mark.parametrize("scenario_case", ScenarioCases.cases)
    @pytest.mark.parametrize(
        "layers_case",
        LayersCases.cases,
    )
    @pytest.mark.slow
    def test_koswat_run_as_sandbox_with_surroundings(
        self,
        input_profile_case,
        scenario_case: KoswatProfileBase,
        layers_case,
        request: pytest.FixtureRequest,
    ):
        # 1. Define test data.
        _test_dir = get_testcase_results_dir(request)
        _csv_surroundings_file = test_data.joinpath(
            "csv_reader", "Omgeving", "T_10_3_bebouwing.csv"
        )
        _shp_trajects_file = test_data.joinpath(
            "shp_reader",
            "Dijkvak",
            "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp",
        )
        assert _csv_surroundings_file.is_file()
        assert _shp_trajects_file.is_file()

        _reinforcement_settings = KoswatReinforcementSettings()
        _new_csv_path = _test_dir.joinpath("10_3", _csv_surroundings_file.name)
        _new_csv_path.parent.mkdir(parents=True)
        _csv_surroundings_file = shutil.copy(_csv_surroundings_file, _new_csv_path)

        # Surroundings wrapper
        _surroundings_section = SurroundingsSectionFom(
            construction_distance=50,
            construction_buffer=10,
            surroundings_database_dir=_test_dir,
            waterside=False,
            buildings=True,
            railways=False,
            waters=False,
        )

        _infrastructure_section = InfrastructureSectionFom(
            infrastructure=False,
            surtax_factor_roads=SurtaxFactorEnum.NORMAAL,
            infrastructure_costs_0dh=InfraCostsEnum.GEEN,
            buffer_waterside=0,
            roads_class2_width=2,
            roads_class24_width=5,
            roads_class47_width=8,
            roads_class7_width=12,
            roads_unknown_width=8,
        )

        _surroundings = SurroundingsWrapperCollectionImporter(
            infrastructure_section_fom=_infrastructure_section,
            surroundings_section_fom=_surroundings_section,
            traject_loc_shp_file=_shp_trajects_file,
            selected_locations=[],
        ).build()[0]

        assert isinstance(scenario_case, KoswatScenario)
        _base_koswat_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=input_profile_case,
                layers_data=layers_case,
                profile_type=KoswatProfileBase,
            )
        ).build()

        # IMPORTANT!!!
        # These are not (entirely) the values from the acceptance `.ini` files!
        _run_settings = KoswatRunScenarioSettings(
            scenario=scenario_case,
            reinforcement_settings=_reinforcement_settings,
            surroundings=_surroundings,
            input_profile_case=_base_koswat_profile,
            costs_setting=KoswatCostsSettings(
                # Set default dike profile costs_setting.
                dike_profile_costs=DikeProfileCostsSettings(
                    added_layer_grass_m3=12.44,
                    added_layer_clay_m3=18.05,
                    added_layer_sand_m3=10.98,
                    reused_layer_grass_m3=6.04,
                    reused_layer_core_m3=4.67,
                    disposed_material_m3=7.07,
                    profiling_layer_grass_m2=0.88,
                    profiling_layer_clay_m2=0.65,
                    profiling_layer_sand_m2=0.60,
                    processing_ground_level_surface_m2=0.25,
                ),
                construction_costs=ConstructionCostsSettings(
                    cb_sheetpile=ConstructionFactors(
                        c_factor=0,
                        d_factor=0,
                        z_factor=999,
                        f_factor=0,
                        g_factor=0,
                    ),
                ),
                surtax_costs=SurtaxCostsSettings(),
            ),
        )

        # 2. Run test
        _summary = KoswatSummaryBuilder(run_scenario_settings=_run_settings).build()
        assert isinstance(_summary, KoswatSummary)

        KoswatSummaryExporter().export(_summary, _test_dir)
        assert _test_dir.joinpath("summary_costs.csv").exists()
        assert _test_dir.joinpath("summary_locations.csv").exists()
        assert _test_dir.joinpath("summary_infrastructure_costs.csv").exists()

        # 3. Verify expectations.
        assert any(_summary.locations_profile_report_list)
        for (
            _reinforcement_profile
        ) in ReinforcementProfileBuilderFactory.get_available_reinforcements():
            assert any(
                isinstance(
                    _rep_profile.profile_cost_report.reinforced_profile,
                    _reinforcement_profile,
                )
                for _rep_profile in _summary.locations_profile_report_list
            ), f"Profile type {_reinforcement_profile.__name__} not found."
        for _multi_report in _summary.locations_profile_report_list:
            _mlp_plot = MultiLocationProfileComparisonPlotExporter()
            _mlp_plot.cost_report = _multi_report
            _mlp_plot.export_dir = _test_dir
            _mlp_plot.export()

        for _multi_report in _summary.locations_profile_report_list:
            assert isinstance(_multi_report, MultiLocationProfileCostReport)
            assert isinstance(_multi_report.profile_cost_report, ProfileCostReport)
            assert _multi_report.total_cost > 0
            assert _multi_report.cost_per_km > 1000
            _layers_report = _multi_report.profile_cost_report.layer_cost_reports
            assert len(_layers_report) == (1 + len(layers_case["coating_layers"]))
            assert all(isinstance(lcr, CostReportProtocol) for lcr in _layers_report)

    @pytest.fixture(
        params=AcceptanceTestScenarioCombinations.get_all_cases(
            acceptance_test_combinations
        )
    )
    def sandbox_acceptance_case(
        self, request: pytest.FixtureRequest
    ) -> tuple[KoswatRunScenarioSettings, Path]:
        _acceptance_test_scenario: AcceptanceTestScenario = request.param
        assert isinstance(_acceptance_test_scenario, AcceptanceTestScenario)

        # 1. Setup acceptance test case
        # Get the reference data in the output directory.
        _results_dir_name = get_fixturerequest_case_name(request)
        _output_dir = test_results.joinpath(
            "sandbox_acceptance_case", _results_dir_name
        )
        if _output_dir.exists():
            shutil.rmtree(_output_dir)
        if _acceptance_test_scenario.reference_data_dir.exists():
            # If it does not exist the test will fail but at least
            # the test results data should be generated.
            shutil.copytree(
                _acceptance_test_scenario.reference_data_dir,
                _output_dir.joinpath("reference"),
            )

        _run_settings = KoswatRunScenarioSettings()
        _run_settings.input_profile_case = _acceptance_test_scenario.profile_case
        _run_settings.scenario = _acceptance_test_scenario.scenario_case
        _run_settings.reinforcement_settings = KoswatReinforcementSettings()
        _run_settings.reinforcement_settings.soil_settings.soil_surtax_factor = (
            SurtaxFactorEnum.NORMAAL
        )
        _run_settings.reinforcement_settings.soil_settings.land_purchase_surtax_factor = (
            SurtaxFactorEnum.NORMAAL
        )
        _run_settings.reinforcement_settings.vps_settings.soil_surtax_factor = (
            SurtaxFactorEnum.NORMAAL
        )
        _run_settings.reinforcement_settings.vps_settings.constructive_surtax_factor = (
            SurtaxFactorEnum.NORMAAL
        )
        _run_settings.reinforcement_settings.vps_settings.land_purchase_surtax_factor = (
            SurtaxFactorEnum.NORMAAL
        )
        _run_settings.reinforcement_settings.vps_settings.polderside_berm_width_vps = 10
        _run_settings.reinforcement_settings.piping_wall_settings.soil_surtax_factor = (
            SurtaxFactorEnum.NORMAAL
        )
        _run_settings.reinforcement_settings.piping_wall_settings.constructive_surtax_factor = (
            SurtaxFactorEnum.NORMAAL
        )
        _run_settings.reinforcement_settings.piping_wall_settings.land_purchase_surtax_factor = (
            SurtaxFactorEnum.NORMAAL
        )
        _run_settings.reinforcement_settings.stability_wall_settings.soil_surtax_factor = (
            SurtaxFactorEnum.MOEILIJK
        )
        _run_settings.reinforcement_settings.stability_wall_settings.constructive_surtax_factor = (
            SurtaxFactorEnum.NORMAAL
        )
        _run_settings.reinforcement_settings.stability_wall_settings.land_purchase_surtax_factor = (
            SurtaxFactorEnum.MOEILIJK
        )
        _run_settings.reinforcement_settings.cofferdam_settings.soil_surtax_factor = (
            SurtaxFactorEnum.MOEILIJK
        )
        _run_settings.reinforcement_settings.cofferdam_settings.constructive_surtax_factor = (
            SurtaxFactorEnum.MOEILIJK
        )
        _run_settings.surroundings = SurroundingsWrapper()
        _run_settings.surroundings.obstacle_surroundings_wrapper.reinforcement_min_buffer = (
            10
        )
        _run_settings.surroundings.obstacle_surroundings_wrapper.reinforcement_min_separation = (
            50
        )
        _run_settings.costs_setting = KoswatCostsSettings()
        _run_settings.costs_setting.dike_profile_costs = DikeProfileCostsSettings()
        _run_settings.costs_setting.dike_profile_costs.added_layer_grass_m3 = 12.44
        _run_settings.costs_setting.dike_profile_costs.added_layer_clay_m3 = 18.05
        _run_settings.costs_setting.dike_profile_costs.added_layer_sand_m3 = 10.98
        _run_settings.costs_setting.dike_profile_costs.reused_layer_grass_m3 = 6.04
        _run_settings.costs_setting.dike_profile_costs.reused_layer_core_m3 = 4.67
        _run_settings.costs_setting.dike_profile_costs.disposed_material_m3 = 7.07
        _run_settings.costs_setting.dike_profile_costs.profiling_layer_grass_m2 = 0.88
        _run_settings.costs_setting.dike_profile_costs.profiling_layer_clay_m2 = 0.65
        _run_settings.costs_setting.dike_profile_costs.profiling_layer_sand_m2 = 0.60
        _run_settings.costs_setting.dike_profile_costs.processing_ground_level_surface_m2 = (
            0.25
        )

        _construction_costs = ConstructionCostsSettings()
        _construction_costs.vzg = ConstructionFactors()
        _construction_costs.vzg.c_factor = 0
        _construction_costs.vzg.d_factor = 0
        _construction_costs.vzg.z_factor = 500
        _construction_costs.vzg.f_factor = 0
        _construction_costs.vzg.g_factor = 0
        _construction_costs.cb_sheetpile = ConstructionFactors()
        _construction_costs.cb_sheetpile.c_factor = 0
        _construction_costs.cb_sheetpile.d_factor = 159.326
        _construction_costs.cb_sheetpile.z_factor = -34.794
        _construction_costs.cb_sheetpile.f_factor = 0
        _construction_costs.cb_sheetpile.g_factor = 0
        _construction_costs.sheetpile_unanchored = ConstructionFactors()
        _construction_costs.sheetpile_unanchored.c_factor = 9.298
        _construction_costs.sheetpile_unanchored.d_factor = 132.239
        _construction_costs.sheetpile_unanchored.z_factor = 103.628
        _construction_costs.sheetpile_unanchored.f_factor = 0
        _construction_costs.sheetpile_unanchored.g_factor = 0
        _construction_costs.sheetpile_anchored = ConstructionFactors()
        _construction_costs.sheetpile_anchored.c_factor = 9.298
        _construction_costs.sheetpile_anchored.d_factor = 150.449
        _construction_costs.sheetpile_anchored.z_factor = 1304.455
        _construction_costs.sheetpile_anchored.f_factor = 0
        _construction_costs.sheetpile_anchored.g_factor = 0
        _construction_costs.diaphragm_wall = ConstructionFactors()
        _construction_costs.diaphragm_wall.c_factor = 0
        _construction_costs.diaphragm_wall.d_factor = 0
        _construction_costs.diaphragm_wall.z_factor = 0
        _construction_costs.diaphragm_wall.f_factor = 281.176
        _construction_costs.diaphragm_wall.g_factor = 1.205
        _construction_costs.cofferdam = ConstructionFactors()
        _construction_costs.cofferdam.c_factor = 0
        _construction_costs.cofferdam.d_factor = 680.782
        _construction_costs.cofferdam.z_factor = -74.602
        _construction_costs.cofferdam.f_factor = 0
        _construction_costs.cofferdam.g_factor = 0
        _run_settings.costs_setting.construction_costs = _construction_costs

        _run_settings.costs_setting.surtax_costs = SurtaxCostsSettings()
        _run_settings.costs_setting.surtax_costs.soil_easy = 2.258
        _run_settings.costs_setting.surtax_costs.soil_normal = 2.509
        _run_settings.costs_setting.surtax_costs.soil_hard = 2.777
        _run_settings.costs_setting.surtax_costs.construction_easy = 2.561
        _run_settings.costs_setting.surtax_costs.construction_normal = 2.912
        _run_settings.costs_setting.surtax_costs.construction_hard = 3.295
        _run_settings.costs_setting.surtax_costs.land_purchase_easy = 1.292
        _run_settings.costs_setting.surtax_costs.land_purchase_normal = 1.412
        _run_settings.costs_setting.surtax_costs.land_purchase_hard = 1.645

        # 2. Run acceptance test case.
        yield _run_settings, _output_dir

    @pytest.mark.slow
    def test_koswat_when_sandbox_given_run_scenario_then_returns_expectation(
        self, sandbox_acceptance_case: tuple[KoswatRunScenarioSettings, Path]
    ):
        # 1. Define test data
        _run_scenario, _export_path_dir = sandbox_acceptance_case
        assert isinstance(_run_scenario, KoswatRunScenarioSettings)

        _reference_dir = _export_path_dir.joinpath("reference")
        for _reference_csv_file in _reference_dir.glob("*.csv"):
            _result_csv_file = _export_path_dir.joinpath(_reference_csv_file.name)
            assert not _result_csv_file.exists()

        _export_figures_path = _export_path_dir.joinpath("figures")
        assert not _export_figures_path.exists()

        # 2. Run test.
        _multi_loc_multi_prof_cost_builder = KoswatSummaryBuilder()
        _multi_loc_multi_prof_cost_builder.run_scenario_settings = _run_scenario
        _summary = _multi_loc_multi_prof_cost_builder.build()

        # 3. Verify final expectations
        assert isinstance(_summary, KoswatSummary)

        # Export results
        KoswatSummaryExporter().export(_summary, _export_path_dir)
        for _multi_report in _summary.locations_profile_report_list:
            _mlp_plot = MultiLocationProfileComparisonPlotExporter()
            _mlp_plot.cost_report = _multi_report
            _mlp_plot.export_dir = _export_figures_path
            _mlp_plot.export()

        assert _export_figures_path.exists()

        # 4. Compare CSV results

        # - check number of files
        _reference_csv_files = list(_reference_dir.glob("*.csv"))
        _result_csv_files = list(_export_path_dir.glob("*.csv"))
        assert len(_result_csv_files) == len(
            _reference_csv_files
        ), f"Expected: {len(_reference_csv_files)} Result: {len(_result_csv_files)}"

        # - check file content
        for _reference_csv_file in _reference_csv_files:
            _result_csv_file = _export_path_dir.joinpath(_reference_csv_file.name)
            assert _result_csv_file.exists(), f"File {_result_csv_file} not found."

            _csv_reference_lines = _reference_csv_file.read_text().splitlines()
            _csv_result_lines = _result_csv_file.read_text().splitlines()
            assert len(_csv_result_lines) == len(
                _csv_reference_lines
            ), f"Difference found in {_result_csv_file.name} in length: Expected: {len(_csv_reference_lines)} Result: {len(_csv_result_lines)}"

            for _idx, _reference_line in enumerate(_csv_reference_lines):
                _line_nr = _idx + 1
                assert (
                    _reference_line == _csv_result_lines[_idx]
                ), f"Difference found in {_result_csv_file.name} at lines:\n [{_line_nr}] Expected: {_reference_line}\n [{_line_nr}]Result: {_csv_result_lines[_idx]}"

        # 5. Compare geometry images.
        def compare_images(reference_img, result_image) -> tuple[float, np.ndarray]:
            # https://www.tutorialspoint.com/how-to-compare-two-images-in-opencv-python
            h, w = reference_img.shape
            diff = cv2.subtract(reference_img, result_image)
            err = np.sum(diff**2)
            # compute mean squared error
            mse = err / (float(h * w))
            return mse, diff

        _glob_filter = "**/*.png"
        assert any(_export_figures_path.glob(_glob_filter))
        for _result_figure in _export_figures_path.glob(_glob_filter):
            _relative_to = _result_figure.relative_to(_export_path_dir)
            _reference_figure = _reference_dir.joinpath(_relative_to)
            _ref_img = cv2.cvtColor(
                cv2.imread(str(_reference_figure)), cv2.COLOR_BGR2GRAY
            )
            _res_img = cv2.cvtColor(cv2.imread(str(_result_figure)), cv2.COLOR_BGR2GRAY)
            _mse, _ = compare_images(_ref_img, _res_img)
            assert _mse == pytest.approx(0.0, rel=1e-6), "Differences for {}".format(
                _relative_to
            )
