# Test strategy `Koswat`

## Overview
We adhere to the standard [V-model](#https://en.wikipedia.org/wiki/V-model_(software_development)).

| Type of test      | Scope         |
|-------------------|---------------|
| Unittests         | Class         |
| Integration tests | Subpackage    |
| System tests      | Package       |
| Acceptance tests  | Requirements  |

These types of tests are described below in the `Koswat` context.

## Unit-/integration tests
For `Koswat` no distinction is made between the unit- and integration test.
The goal of the unit- and integration tests is to validate the behavior of separate classes or subpackages.
In general they don't require data input or output unless that is what the class is about.

## System tests
The goal of the system tests is to validate the outer behavior of the package is as expected.
The system tests can be found in `tests\test_main.py`.

Possible improvements:
- Mark the tests as `system`.
- Strip the test to only test the outer behavior (can package be installed and run, is logging created).

## Acceptance tests
The goal of the acceptance tests is to test if the overall behavior of the application is according to requirements.
The full workflow is executed and the output is validated.
As these tests take relatively much time to be executed, they are marked as `slow`.
The system tests can be found in `tests\test_acceptance.py`.

Possible improvements:
- Add docstrings to the fixtures and classes used, describing the purpose and usage.

### Sandbox tests
Several cases are tested, which are defined in `acceptance_test_scenario_cases`.
A case combines a dike profile (`AcceptanceTestInputProfileCases`) with layers (`LayersCases`) and scenarios (`ScenarioCases*`).

Goal: Validate a Koswat run generates the correct results.

Inputs:
- Realistic run settings (defined in `sandbox_acceptance_case`).
- NO locations and NO surroundings.

Validations:
- Check if the generated geometry images (`.png`) are identical to the provided reference images.
- Check is the generated exports (`.csv`) are identical to the provided reference files.

Possible improvements:
- Add a limited number of locations.

### Surroundings tests
A limited number of cases is tested, using the default dike profile (`InputProfileCases`) with 2 layer cases (`LayersCases`) and 3 different scenarios (`ScenarioCases`).

Goal: TODO

Inputs:
- Realistic run settings.
- Obstacles (NO infrastructures) from `test_data\csv_reader\Omgeving\T_10_3_bebouwing.csv`
- Locations from `test_data\shp_reader\Dijkvak\Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp`.

Validations:
- Rough check on the presence of valid outputs:
  - Have all profiles been calculated?
  - Have all the expected .csv-files been created?

Possible improvements:
- Remove as they are superseded by the [Obstance and infrastructure tests](#Obstance-and-infrastructure-tests)?

### Obstacle and infrastructure tests
A limited number of cases is tested, using the default dike profile (`InputProfileCases`) with 2 layer cases (`LayersCases`) and 3 different scenarios (`ScenarioCases`). These are combined with 4 different surrounding scenarios with and without infrastructure and/or obstacles.

Goal: Validate the calculations for locations with obstacles and infrastructures work correctly.

Inputs:
- Configs from `koswat_general.ini` and `koswat_costs.ini` in `test_data\acceptance`.
- Surroundings from `test_data\acceptance\surroundings_analysis\10_3`.
- Locations from `test_data\shp_reader\Dijkvak\Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp`.

Validations:
- Rough check on the presence of valid outputs:
  - Have all the expected .csv-files been created?
  - Are any surrouding reports (obstacles and/or infrastructure) present?

Possible improvements:
- Reduce the number of cases?
- Reduce the number of locations?
- Check content of .csv-files
