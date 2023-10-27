# Strategies

This modules contains the logic to choose which measure will be applied for a given dike traject. A strategy follows the `StraetgyProtocol` and it's applied with the method `apply_strategy`, which expects a strategy input (`StrategyInput`) and returns a mapping (`StrategyLocationReinforcement`) between a location(`PointSurroundings`) and the selected reinforcement (`ReinforcementProtocol`) .

- `StrategyInput`, wraps all required properties to apply a strategy: 
    - locations_matrix (`dict[PointSurroundings, list[Type[ReinforcementProfileProtocol]]]`), contains all the available reinforcements that can be applied at each location.
    - structure_min_buffer (`float`), how many extra meters a structure requires for support its reinforcement.
    - structure_min_length (`float`), how many minimal meters are required for a structure to "exist". This rule can, at times, have certain exceptions.

- `StrategyLocationReinforcement`, represents a mapped location to a selected measure.
    - location (`PointSurroundings`), a point (meter) in the dike traject.
    - selected_measure (`Type[ReinforcementProfileProtocol]`), which is the reinforcement that should be applied to the location.
    - available_measure (`list[Type[ReinforcementProfileProtocol]]`), which are the possible reinforcements that could be applied to the location.


(`structure_min_buffer`) and minimal structure length (`structure_min_length`).

## Available strategies.

### Order based (default). 
A strategy is chosen based on a fix priority order:
1. `SoilReinforcement`
2. `PipingWallReinforcement`
3. `StabilityWallReinforcement`
4. `CofferDamReinforcement`

