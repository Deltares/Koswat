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

- Originally all our reinforcements have been defined based on a 'polderside' perspective. For waterside calculations we use the same calculated reinforcement profiles (except for `SoilReinforcementProfile`). We commonly name them as 'flexible' (or non-fixed).

- We therefore consider a reinforcement to be 'suitable' for a given traject point when there is enough space between the waterside and dikeside obstacles, therefore only looking at the total 'length' of the profile (`x` axis value of the reinforcement's geometry). This applies to all reinforcement types except for soil reinforcement.
    - In 'the real world', it will imply that a given reinforcement might have to be moved closer to the water- or polderside.
    - The required displacement is not displayed nor saved anywhere as koswat focuses on assigning the cheapest / most suitable dike reinforcement for a whole traject.

