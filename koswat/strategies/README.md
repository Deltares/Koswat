# Strategies

This modules contains the logic to choose which measure will be applied for a given dike traject. A strategy follows the `StrategyProtocol` and it's applied with the method `apply_strategy`, which expects a strategy input (`StrategyInput`) and returns a mapping (`StrategyLocationReinforcement`) between a location(`PointSurroundings`) and the selected reinforcement (`ReinforcementProtocol`) .

- `StrategyInput`, wraps all required properties to apply a strategy: 
    - locations_matrix (`dict[PointSurroundings, list[Type[ReinforcementProfileProtocol]]]`), contains all the available reinforcements that can be applied at each location.
    - structure_min_buffer (`float`), how many extra meters a structure requires for support its reinforcement.
    - structure_min_length (`float`), how many minimal meters are required for a structure to "exist". This rule can, at times, have certain exceptions.

- `StrategyLocationReinforcement`, represents a mapped location to a selected measure.
    - location (`PointSurroundings`), a point (meter) in the dike traject.
    - selected_measure (`Type[ReinforcementProfileProtocol]`), which is the reinforcement that should be applied to the location.
    - available_measures (`list[Type[ReinforcementProfileProtocol]]`), which are the possible reinforcements that could be applied to the location.


## Available strategies

The following strategies are currently available, please refer to the official documentation for a more in-detail explanation of each of them

- [__Default__] Order based. A strategy is chosen based on a pre-defined measure priority order.

