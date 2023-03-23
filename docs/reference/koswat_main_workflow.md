# Main workflow

As described in the [user manual](../user_manual.md), the tool can be used either as a sandbox, where the user has responsibility on how to put together an analysis, or as a command line tool. 

When using the latter unfortunately we will only have one available call, in this chapter we will breakdown this main workflow so that we can better understand the structure of the rest of the package.

First of all, let's write the workflow as a pipeline:

`CLI call -> Import of ini files -> Run scenarios -> [Generate reinforcement profiles -> Calculate costs -> Export results]`

|![General Workflow](./imgs/general_workflow.png)|
|:--:|
|Image 1. General Workflow|

## CLI Call

This step is very straightforward, the command line will run the method `run_analysis`, which will initiate the `KoswatHandler` and start an analysis.

## Import of ini files
This step comprehends of several more steps. Usually, for each of the file imports an internal workflow will happen:

`File -> Import -> File Object Model -> Build -> Data Object Model`

This step is summarized by the generation of the `KoswatRunSettings` object.

## Run scenarios
Each `KoswatRunScenarioSettings` will run a koswat analysis for a given dike section.
To do so, a specific `KoswatProfileBase` will be created based on the conditions from the `KoswatScenario` and the surroundings of said dike section.

## Generate reinforcement profiles
All reinforcement profiles will be calculated for the scenario `KoswatProfileBase` profile. 

## Calculate costs
For this step, we will be creating a [cost report](koswat_cost_report.md)
For each of the reinforcement profiles we will calculate their associated costs only when the surroundings allow it.

## Export results
Once the costs reports are generate each of the summaries is exported to a `*.csv` file whilst the reinforcement profiles 'layers' are also exported into different `*.png` files.

