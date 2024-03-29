from __future__ import annotations

import shutil
from pathlib import Path

import cv2
import numpy as np
import pytest

from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.io.koswat_surroundings_importer import (
    KoswatSurroundingsImporter,
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
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.cost_report.cost_report_protocol import CostReportProtocol
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
from tests import (
    get_fixturerequest_case_name,
    get_testcase_results_dir,
    test_data,
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
            "csv_reader", "Omgeving", "T_10_3_bebouwing_binnendijks.csv"
        )
        _shp_trajects_file = test_data.joinpath(
            "shp_reader",
            "Dijkvak",
            "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp",
        )
        assert _csv_surroundings_file.is_file()
        assert _shp_trajects_file.is_file()

        _reinforcement_settings = KoswatReinforcementSettings()
        _surroundings_importer = KoswatSurroundingsImporter()
        _new_csv_path = _test_dir.joinpath("10_3", _csv_surroundings_file.name)
        _new_csv_path.parent.mkdir(parents=True)
        _csv_surroundings_file = shutil.copy(_csv_surroundings_file, _new_csv_path)
        _surroundings_section = SurroundingsSectionFom()
        _surroundings_section.constructieafstand = 50
        _surroundings_section.constructieovergang = 10
        _surroundings_section.surroundings_database_dir = _test_dir
        _surroundings_section.buitendijks = False
        _surroundings_section.bebouwing = True
        _surroundings_section.spoorwegen = False
        _surroundings_section.water = False
        _surroundings_importer.traject_loc_shp_file = _shp_trajects_file
        _surroundings = _surroundings_importer.import_from(_surroundings_section)[0]

        assert isinstance(scenario_case, KoswatScenario)
        _base_koswat_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=input_profile_case,
                layers_data=layers_case,
                profile_type=KoswatProfileBase,
            )
        ).build()

        _run_settings = KoswatRunScenarioSettings()
        _run_settings.scenario = scenario_case
        _run_settings.reinforcement_settings = _reinforcement_settings
        _run_settings.surroundings = _surroundings
        _run_settings.input_profile_case = _base_koswat_profile
        _costs_settings = KoswatCostsSettings()
        _run_settings.costs_setting = _costs_settings
        # Set default dike profile costs_setting.
        _costs_settings.dike_profile_costs = DikeProfileCostsSettings()
        _costs_settings.dike_profile_costs.added_layer_grass_m3 = 12.44
        _costs_settings.dike_profile_costs.added_layer_clay_m3 = 18.05
        _costs_settings.dike_profile_costs.added_layer_sand_m3 = 10.98
        _costs_settings.dike_profile_costs.reused_layer_grass_m3 = 6.04
        _costs_settings.dike_profile_costs.reused_layer_core_m3 = 4.67
        _costs_settings.dike_profile_costs.disposed_material_m3 = 7.07
        _costs_settings.dike_profile_costs.profiling_layer_grass_m2 = 0.88
        _costs_settings.dike_profile_costs.profiling_layer_clay_m2 = 0.65
        _costs_settings.dike_profile_costs.profiling_layer_sand_m2 = 0.60
        _costs_settings.dike_profile_costs.bewerken_maaiveld_m2 = 0.25
        _costs_settings.construction_costs = ConstructionCostsSettings()
        _costs_settings.construction_costs.cb_damwand = ConstructionFactors()
        _costs_settings.construction_costs.cb_damwand.c_factor = 0
        _costs_settings.construction_costs.cb_damwand.d_factor = 0
        _costs_settings.construction_costs.cb_damwand.z_factor = 999
        _costs_settings.construction_costs.cb_damwand.f_factor = 0
        _costs_settings.construction_costs.cb_damwand.g_factor = 0
        _costs_settings.surtax_costs = SurtaxCostsSettings()

        # 2. Run test
        _multi_loc_multi_prof_cost_builder = KoswatSummaryBuilder()
        _multi_loc_multi_prof_cost_builder.run_scenario_settings = _run_settings
        _summary = _multi_loc_multi_prof_cost_builder.build()
        assert isinstance(_summary, KoswatSummary)

        KoswatSummaryExporter().export(_summary, _test_dir)
        assert _test_dir.joinpath("summary_costs.csv").exists()
        assert _test_dir.joinpath("summary_locations.csv").exists()

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
        # Get the refernce data in the output directory.
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
        _run_settings.surroundings.reinforcement_min_buffer = 10
        _run_settings.surroundings.reinforcement_min_separation = 50
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
        _run_settings.costs_setting.dike_profile_costs.bewerken_maaiveld_m2 = 0.25

        _construction_costs = ConstructionCostsSettings()
        _construction_costs.cb_damwand = ConstructionFactors()
        _construction_costs.cb_damwand.c_factor = 0
        _construction_costs.cb_damwand.d_factor = 159.326
        _construction_costs.cb_damwand.z_factor = -34.794
        _construction_costs.cb_damwand.f_factor = 0
        _construction_costs.cb_damwand.g_factor = 0
        _construction_costs.damwand_onverankerd = ConstructionFactors()
        _construction_costs.damwand_onverankerd.c_factor = 9.298
        _construction_costs.damwand_onverankerd.d_factor = 132.239
        _construction_costs.damwand_onverankerd.z_factor = 103.628
        _construction_costs.damwand_onverankerd.f_factor = 0
        _construction_costs.damwand_onverankerd.g_factor = 0
        _construction_costs.damwand_verankerd = ConstructionFactors()
        _construction_costs.damwand_verankerd.c_factor = 9.298
        _construction_costs.damwand_verankerd.d_factor = 150.449
        _construction_costs.damwand_verankerd.z_factor = 1304.455
        _construction_costs.damwand_verankerd.f_factor = 0
        _construction_costs.damwand_verankerd.g_factor = 0
        _construction_costs.diepwand = ConstructionFactors()
        _construction_costs.diepwand.c_factor = 0
        _construction_costs.diepwand.d_factor = 0
        _construction_costs.diepwand.z_factor = 0
        _construction_costs.diepwand.f_factor = 281.176
        _construction_costs.diepwand.g_factor = 1.205
        _construction_costs.kistdam = ConstructionFactors()
        _construction_costs.kistdam.c_factor = 0
        _construction_costs.kistdam.d_factor = 680.782
        _construction_costs.kistdam.z_factor = -74.602
        _construction_costs.kistdam.f_factor = 0
        _construction_costs.kistdam.g_factor = 0
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

        _export_summary_costs_path = _export_path_dir.joinpath("summary_costs.csv")
        assert not _export_summary_costs_path.exists()

        _export_summary_locations_path = _export_path_dir.joinpath(
            "summary_locations.csv"
        )
        assert not _export_summary_locations_path.exists()

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
        _reference_dir = _export_path_dir.joinpath("reference")
        assert _export_summary_costs_path.exists()

        _csv_summary_costs_lines = _export_summary_costs_path.read_text().splitlines()
        _csv_reference_lines = (
            _reference_dir.joinpath(_export_summary_costs_path.name)
            .read_text()
            .splitlines()
        )
        for _idx, _reference_line in enumerate(_csv_reference_lines):
            _line_nr = _idx + 1
            assert (
                _reference_line == _csv_summary_costs_lines[_idx]
            ), f"CSV Summary difference found at lines:\n [{_line_nr}] Expected: {_reference_line}\n [{_line_nr}]Result: {_csv_summary_costs_lines[_idx]}"

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
