# Strategies

This modules contains the logic to choose which measure will be applied for a given dike traject. A strategy follows the `StrategyProtocol` and it's applied with the method `apply_strategy`, which expects a strategy input (`StrategyInput`) and returns a mapping (`StrategyLocationReinforcement`) between a location(`PointSurroundings`) and the selected reinforcement (`ReinforcementProtocol`) .

- `StrategyInput`, wraps all required properties to apply a strategy: 
    - strategy_locations (`list[StrategyLocationInput]`), contains all the available reinforcements that can be applied at each location and their related costs.
    - structure_min_buffer (`float`), how many extra meters a structure requires to support its reinforcement.
    - structure_min_length (`float`), how many minimal meters are required for a structure to "exist". This rule can, at times, have certain exceptions.

- `StrategyLocationInput`, gathers all the input required for a strategy to determine which reinforcement can be applied based on its location (`point_surrounding`) and `available_reinforcements`.
    - point_surrounding (`PointSurroundings`), a point (meter) in the dike traject.
    - strategy_reinforcement_type_costs (`list[StrategyReinforcementTypeCosts]`), all the reinforcements that can be used at this location and their related costs.
    - cheapest_reinforcement (`StrategyReinforcementTypeCosts`), returns which "available reinforcment" has the lower total costs at this location.
    - available_measures (`Type[ReinforcementProfileProtocol]`), returns only the reinforcement type from the `strategy_reinforcement_type_costs` collection.

- `StrategyReinforcementTypeCosts`, maps a type of reinforcement to the calculated costs from the `cost_report` subproject.
    - reinforcement_type (`Type[ReinforcementProfileProtocol]`), the mapped reinforcement type.
    - base_costs (`float`), the costs only related to the reinforcement's required space (thus excluding infrastructure costs).
    - infrastructure_costs (`float`), the costs associated **only** to infrastructures.
    - total_costs (`float`), the addition of `base_costs` and `infrastructure_costs`.

- `StrategyLocationReinforcement`, represents a mapped location to a selected measure.
    - location (`PointSurroundings`), a point (meter) in the dike traject.
    - selected_measure (`Type[ReinforcementProfileProtocol]`), which is the reinforcement that should be applied to the location.
    - available_measures (`list[Type[ReinforcementProfileProtocol]]`), which are the possible reinforcements that could be applied to the location.
    - strategy_location_input (`StrategyLocationInput`), the related input with available reinforcements and their costs related to this location-measure mapping.


## Available strategies

The following strategies are currently available, please refer to the official documentation for a more in-detail explanation of each of them

- [__Default__] Order based. A strategy is chosen based on a pre-defined measure priority order.

