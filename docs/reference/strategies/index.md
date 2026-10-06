# About strategies

Koswat can determine which is the "best" reinforcement type for a dike traject based on different selection criteria that we name "strategies" (`StrategyProtocol`).

A strategy requires a strategy input (`StrategyInput`), this input contains information over which reinforcement types are available at each location as well as what's the __minimal buffer__ (`reinforcement_min_buffer`) and __minimal length__ (`reinforcement_min_length`)  for each reinforcement type.

By default a strategy is applied as follows:

1. For each point (meter) in the traject, determine which reinforcements can be applied to it.
2. Choose one of the available reinforcements based on the chosen [strategy](./order_based.md). When no reinforcement is available the most restrictive will be chosen (`CofferDam`).
3. Apply a buffer (`reinforcement_min_buffer`) for each one of the reinforcements.
4. Check if the minimal distance between constructions is met (`reinforcement_min_length`), otherwise change it into one of the reinforcements next to it.
5. Repeat 4 until all reinforcements have enough distance between themselves.
6. Find based on the strategy for [infrastructure derived costs](./infrastructure_priority.md), mapped locations (`list[StrategyLocationReinforcement]`) whose reinforcement can be increased into a most restrictive one with total lower costs. 
7. Return list of mapped locations (`list[StrategyLocationReinforcement]`).

## Available strategies

Currently the following strategies are implemented:

- [Order based](./order_based.md)
- [Infrastructure priority](./infrastructure_priority.md), by default the strategy to run during a Koswat analysis.

## Design decisions

### 'Fixed' and 'flexible' reinforcements

Originally, all reinforcement profiles were defined on the polder side, meaning that their geometries extend along the polder rather than the waterside. For waterside analyses, the same calculated reinforcement profiles are reused (with the exception of `SoilReinforcementProfile`). Although their geometry is defined on the polder side, these profiles are commonly referred to as “flexible” or “non-fixed,” because they may also be applied on the waterside.

Accordingly, a reinforcement is considered suitable at a given trajectory point only when sufficient space is available between the waterside and dikeside constraints, based solely on the total profile width (i.e., the x-axis extent of the reinforcement geometry). This criterion applies to all reinforcement types except soil reinforcement.

In practical terms, this means that a given reinforcement may need to be shifted closer to the water or to the dike toe. This displacement is neither displayed nor stored explicitly, since the objective of KOSWAT is to assign the most cost-effective and appropriate dike reinforcement for an entire trajectory.

