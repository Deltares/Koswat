# Koswat package installation

## Requirements

This step requires that you have koswat installed as a package. If not, please check [our installation documentation](https://deltares.github.io/Koswat/installation.html)

## Running 

Assuming a correct installation, you can now run koswat via python command line.

So let's run it based on our `basic_case` example

```console
C:\> python -m koswat --input_file basic_case\koswat_general.json
2025-11-26 10:24:32 AM - [koswat_handler.py:119] - root - INFO - Initialized Koswat.
2025-11-26 10:24:32 AM - [koswat_run_settings_importer.py:70] - root - INFO - Importing CSV configuration from basic_case\koswat_general.json
2025-11-26 10:24:32 AM - [koswat_costs_importer.py:41] - root - INFO - Importing costs settings from basic_case\koswat_costs.json.
...
2025-11-26 10:24:45 AM - [koswat_handler.py:59] - root - INFO - Exported summary results to: basic_case\results_output\dike_10-1-1-A-1-A\scenario_scenario2
2025-11-26 10:24:46 AM - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: basic_case\results_output\dike_10-1-1-A-1-A\scenario_scenario2
2025-11-26 10:24:46 AM - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: basic_case\results_output\dike_10-1-1-A-1-A\scenario_scenario2
2025-11-26 10:24:47 AM - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: basic_case\results_output\dike_10-1-1-A-1-A\scenario_scenario2
2025-11-26 10:24:47 AM - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: basic_case\results_output\dike_10-1-1-A-1-A\scenario_scenario2
2025-11-26 10:24:47 AM - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: basic_case\results_output\dike_10-1-1-A-1-A\scenario_scenario2
2025-11-26 10:24:47 AM - [koswat_handler.py:123] - root - INFO - Finalized Koswat.
```