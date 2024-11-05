# Strategies

This modules contains the logic to choose which measure will be applied for a given dike traject. A strategy follows the `StrategyProtocol` and it's applied with the method `apply_strategy`, which expects a strategy input (`StrategyInput`) and returns a mapping (`StrategyLocationReinforcement`) between a location(`PointSurroundings`) and the selected reinforcement (`ReinforcementProfileProtocol`) .

- `StrategyInput`, wraps all required properties to apply a strategy: 
    - strategy_locations (`list[StrategyLocationInput]`), contains all the available reinforcements that can be applied at each location and their related costs.
    - strategy_reinforcements (`list[StrategyReinforcementInput]`), all the reinforcements that can be used at this location and their related costs and width.
    - structure_min_buffer (`float`), how many extra meters a structure requires to support its reinforcement.
    - structure_min_length (`float`), how many minimal meters are required for a structure to "exist". This rule can, at times, have certain exceptions.

- `StrategyLocationInput`, gathers all the input required for a strategy to determine which reinforcement can be applied based on its location (`point_surrounding`) and `available_reinforcements`.
    - point_surrounding (`PointSurroundings`), a point (meter) in the dike traject.
    - strategy_reinforcement_type_costs (`list[StrategyReinforcementTypeCosts]`), all the reinforcements that can be used at this location and their related cost.
    - cheapest_reinforcement (`StrategyReinforcementTypeCosts`), returns which "available reinforcment" has the lower total costs at this location.
    - available_measures (`Type[ReinforcementProfileProtocol]`), returns only the reinforcement type from the `strategy_reinforcement_type_costs` collection.

- `StrategyReinforcementTypeCosts`, maps a type of reinforcement to the calculated costs from the `cost_report` subproject.
    - reinforcement_type (`Type[ReinforcementProfileProtocol]`), the mapped reinforcement type.
    - base_costs (`float`), the costs only related to the reinforcement's required space (thus excluding infrastructure costs).
    - infrastructure_costs (`float`), the costs associated **only** to infrastructures.
    - total_costs (`float`), the addition of `base_costs` and `infrastructure_costs`.

- `StrategyReinforcementInput`, contains the reinforcement types that are relevant to the strategy, as they were selected for one or more locations included in the strategy.
    - reinforcement_type (`Type[ReinforcementProfileProtocol]`), the mapped reinforcement type.
    - base_costs (`float`), the costs only related to the reinforcement's required space (thus excluding infrastructure costs).
    - ground_level_surface (`float`), profile's width from waterside crest point.

- `StrategyLocationReinforcement`, represents a mapped location to a selected measure.
    - location (`PointSurroundings`), a point (meter) in the dike traject.
    - current_selected_measure (`Type[ReinforcementProfileProtocol]`), which is the reinforcement that should be applied to the location.
    - available_measures (`list[Type[ReinforcementProfileProtocol]]`), which are the possible reinforcements that could be applied to the location.
    - strategy_location_input (`StrategyLocationInput`), the related input with available reinforcements and their costs related to this location-measure mapping.

- `StrategyStepAssignment`, helps keep track of the different `StrategyLocationReinforcement.current_selected_measure` values done at each strategy.

## Available strategies

The following strategies are currently available, please refer to the official documentation for a more in-detail explanation of each of them:

- Order based (`OrderBased`). A strategy is chosen based on a dynamically determined order of reinforcements. This order is determined from least to most restrictive, where reinforcements are omitted when they are less restrictive and more expensive than other reinforcement(s). Cofferdam is forced as the last reinforcement of this order.
- [__Default__] Infra-priority based (`InfraPriorityStrategy`). Clusters are created based on the cheapest total cost (including infrastructure reworks). This strategy is applied __after__  _Order based_, the clusters are then modified into a reinforcement that requires less space (thus more expensive) but induce less infrastructure costs, therefore becoming cheaper. We apply this strategy based on sub-clusters, this means that only at a specific contiguous subset of locations the new reinforcement will be applied, therefore optimizing costs.

