# Cost Report

This module contains all possible definitions concerning the generation of a cost-report (`CostReportProtocol`).

The defined hierarchy is such as: 
- `KoswatSummary`: Wrapper of all multi-location-profile-cost-reports `MultiLocationProfileCostReport`.
- `MultiLocationproFileCostReport`: Generates a profile-cost-report `ProfileCostReport`, based on a list of locations `PointSurroundings` and the compatible reinforcement profiles `ReinforcementProfileProtocol`.
- `ProfileCostReport`: Contains a summary of the costs associated with its reinforced profile (`ReinforcementProfileProtocol`). It also contains a list of reports per-layer ( `LayerCostReport`).
- `LayerCostReport`: A brief summary of the associated volumes and costs for a given `ReinforcementLayerProtocol`.