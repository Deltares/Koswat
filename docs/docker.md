# Docker

Koswat can also be used via command line tool with [docker](https://www.docker.com/) or [podman](https://podman.io/). To do so you will have first to [build the image](#build-koswat-docker-image) and then [run the built container](#run-koswat-docker-container).

!!! note
    This guideline assumes you have a podman installation, when using docker you only need to replace our `podman` command with `docker`.

## Build koswat docker image

The koswat container needs to be built before we can run it, this is not strictly necessary when running a remote image (check [the following step](#run-koswat-docker-container)), but we will check either way how to build either a local or a remote image.

- From a local koswat checkout:
    ```console
    cd {your_local_koswat_checkout}
    podman build -t koswat .
    ```

- From our Deltares registry (as mentioned this step is not really needed):
```console
podman pull containers.deltares.nl/gfs/koswat:latest
```

## Run koswat docker container

You can now proceed to run the tool, we will make use of our example data ( `examples/basic_case` ), so you can copy it to a local test directory (`{your_data_to_run_directory}`).

Running through docker requires that we **mount** the model data that we will use, this is done with the flag `-v {your_data_location}:/{mounted_data_location}`. 

!!! important
    At the moment this docker requires that all the paths defined in the `koswat_general.json` are relative to the mounted data. So in our case we  had to modify them such as `Dijksecties_Selectie = /run_data/koswat_dike_selection.txt` and so on for each of them.
    Otherwise __it will not work__.

- With your local image:
    ```console
    podman run -it -v {your_data_to_run_directory}:/run_data koswat --input_file /run_data/koswat_general.json
    ```
- Or using the remote image instead:
    ```console
    podman run -it -v {your_data_to_run_directory}:/run_data containers.deltares.nl/gfs/koswat:latest --input_file /run_data/koswat_general.json
    ```

Which will result in something like this:
```console
{date and time} - [koswat_handler.py:119] - root - INFO - Initialized Koswat.                                                                                             
{date and time} - [koswat_run_settings_importer.py:70] - root - INFO - Importing CSV configuration from /test_data/koswat_general.json                                     
{date and time} - [koswat_costs_importer.py:41] - root - INFO - Importing costs settings from /test_data/koswat_costs.json.                                                
{date and time} - [koswat_run_settings_importer.py:100] - root - INFO - Importing JSON configuration completed.                                                            
{date and time} - [koswat_run_settings_importer.py:103] - root - INFO - Mapping data to Koswat Settings
{date and time} - [koswat_run_settings_importer.py:158] - root - INFO - Creating scenarios for profile 10-1-1-A-1-A.
{date and time} - [koswat_run_settings_importer.py:171] - root - INFO - Created sub scenario Scenario1.
{date and time} - [koswat_run_settings_importer.py:171] - root - INFO - Created sub scenario Scenario2.
{date and time} - [koswat_run_settings_importer.py:140] - root - WARNING - No scenario found for selected section 10-1-2-A-1-A.
{date and time} - [koswat_run_settings_importer.py:140] - root - WARNING - No scenario found for selected section 10-1-3-A-1-B-1.
{date and time} - [koswat_run_settings_importer.py:174] - root - INFO - Finished generating koswat scenarios. A total of 2 scenarios were created.
{date and time} - [koswat_run_settings_importer.py:112] - root - INFO - Settings import completed.
...
{date and time} - [koswat_handler.py:59] - root - INFO - Exported summary results to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:123] - root - INFO - Finalized Koswat.
```
