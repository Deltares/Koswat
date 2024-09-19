# Cost Report

This module contains all possible definitions concerning the generation of a cost-report (`CostReportProtocol`).

A cost report is generated given a `KoswatRunScenarioSettings` instance. Said report will only consider the `ReinforcementProfileProtocol` instances which are suitable for the provided surroundings (`SurroundingsWrapper`).

In addition to the cost report, an infrastructure report (`InfrastructureLocationProfileCostReport`) will be added based on the `InfrastructureSurroundingsWrapper` which will determine additional costs per reinforcment depending on whether the infrastructures need to be replaced or repaired.

The defined hierarchy is such as: 
- `KoswatSummary`: Wrapper of all multi-location-profile-cost-reports `MultiLocationProfileCostReport`.
- `MultiLocationproFileCostReport`: Generates a profile-cost-report `ProfileCostReport`, based on a list of locations `PointSurroundings` and the compatible reinforcement profiles `ReinforcementProfileProtocol`.
- `ProfileCostReport`: Contains a summary of the costs associated with its reinforced profile (`ReinforcementProfileProtocol`). It also contains a list of reports per-layer ( `LayerCostReport`).
- `LayerCostReport`: A brief summary of the associated volumes and costs for a given `ReinforcementLayerProtocol`.