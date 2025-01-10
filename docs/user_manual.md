# User manual

## As a command line tool
When using `Koswat` as a package you can run it directly from the command line as follows:

```cli
python -m koswat --input_file path\\to\\your\\koswat.ini --log_output path\\to\\your\\output\\dir
```
The arguments are:

- `--input_file` (required): Absolute path to the location of your general `koswat.ini` file.
- `--log_output` (optional): Absolute path to the location of where the `koswat.log` will be written. If not specified it will be written at the root of the execution directory.

It is also possible to check all the above possibilities via the `--help` argument in the command line:
```cli
python -m koswat --help
```

## As a sandbox
It is entirely possible to make a custom Koswat analysis using the tool as a sandbox. This means, through a script calling the different classes to generate an analysis.

As a simple example, we can rewrite the acceptance test `test_given_surrounding_files_run_calculations_for_all_included_profiles`:

```python
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.profile import KoswatProfileBase, KoswatProfileBuilder
from koswat.cost_report.summary import KoswatSummary, KoswatSummaryBuilder
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.cost_report.io.summary.koswat_summary_exporter import KoswatSummaryExporter
from koswat.cost_report.io.plots.multi_location_profile_comparison_plot_exporter import (
    MultiLocationProfileComparisonPlotExporter,
)
from koswat.dike_reinforcements import ReinforcementProfileBuilderFactory

# 1. Define input data.
_input_dir = Path("C:\\my_koswat_input_dir")
_output_dir = Path("C:\\my_koswat_results")
_shp_trajects_file = (
    _input_dir
    / "Dijkvak"
    / "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp"
)
assert _shp_trajects_file.is_file()

## Define input profile case
input_profile_case = KoswatInputProfileBase()
input_profile_case.dike_section = "test_data"
input_profile_case.waterside_ground_level = 0
input_profile_case.waterside_slope = 3
input_profile_case.waterside_berm_width = 0
input_profile_case.waterside_berm_height = 0
input_profile_case.crest_height = 6
input_profile_case.crest_width = 5
input_profile_case.polderside_slope = 3
input_profile_case.polderside_berm_height = 0
input_profile_case.polderside_berm_width = 0
input_profile_case.polderside_ground_level = 0
input_profile_case.pleistocene = -5
input_profile_case.aquifer = -2

## Define the scenario case
scenario_case = KoswatScenario()
scenario_case.scenario_name = ""
scenario_case.scenario_section = ""
scenario_case.d_h = 1
scenario_case.d_s = 10
scenario_case.d_p = 30
scenario_case.crest_width = 5
scenario_case.waterside_slope = 3

## Define the layers case
layers_case = dict(
        base_layer=dict(material=KoswatMaterialType.SAND),
        coating_layers=[
            dict(material=KoswatMaterialType.GRASS, depth=0.3),
            dict(material=KoswatMaterialType.CLAY, depth=0.5),
        ],
    )

## Import surroundings (TODO: update with latest implementation of SurroundingsWrapperCollectionImporter)
_surroundings_importer = KoswatSurroundingsImporter()
_surroundings_importer.traject_loc_shp_file = _shp_trajects_file
_surroundings = _surroundings_importer.import_from(_test_dir)[0]

assert isinstance(scenario_case, KoswatScenario)
_base_koswat_profile = KoswatProfileBuilder.with_data(
    dict(
        input_profile_data=input_profile_case,
        layers_data=layers_case,
        profile_type=KoswatProfileBase,
    )
).build()

## Define the run settings based on the previous calculated parameters.
_run_settings = KoswatRunScenarioSettings()
_run_settings.scenario = scenario_case
_run_settings.surroundings = _surroundings
_run_settings.input_profile_case = _base_koswat_profile

# 2. Run summary
_multi_loc_multi_prof_cost_builder = KoswatSummaryBuilder()
_multi_loc_multi_prof_cost_builder.run_scenario_settings = _run_settings
_summary = _multi_loc_multi_prof_cost_builder.build()

KoswatSummaryExporter().export(_summary, _output_dir)

# 3. Generate plots
assert isinstance(_summary, KoswatSummary)
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
    _mlp_plot.export_dir = _output_dir
    _mlp_plot.export()

```