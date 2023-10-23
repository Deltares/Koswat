# Calculations

This module contains the information on calculating a reinforcement (`ReinforcementProfileCalculationProtocol`) for a Profile (`KoswatProfileProtocol`) resulting in a 'Reinforced' Profile (`ReinforcementProfileProtocol`). It is divided in submodules representing the different types of reinforcements and their builders.

The module is divided as:
- __io__: Input / output module containing the concrete importers and exporters for the models here defined.
- __reinforcement_layers__: Module containing the definition of all `ReinforcementLayerProtocol` implementations and their builders.
- __outside_slope_reinforcement__: Module containing the definition of all `OutsideSlopeReinforcementProfile` implementations and their builders.
- __standard_reinforcement__: Module containing the definition of all `StandardReinforcementProfile` implementations and their builders.
- __protocols__: Module where the `typing.Protocol` concrete definitions used across the whole calculation modules are saved.

At  the same time we expose directly the 
- `ReinforcementProfileBuilderFactory`: Factory to retrieve the correct instances of a `ReinforcementProfileBuilderProtocol`.

## Design decisions.
It could be argued that some of the code could be reduced by using abstractions or simple inheritance. However I opted for 'duplicating' methods logic in order to reduce the dependency between classes thus making them totally independent. Alas the usage of protocols over abstractions.

A reinforcement calculation will naturally be found in its respective `*_profile_calculation.py` file. This way we isolate the logic to get each one of the values that compose a specific reinforcement profile, allowing us for better maintainability and verification.

## Future work.
After a few iterations of adding / modifying how a reinforcement is calculated, it is preferred to refactor the process by splitting the process into two steps:
1. Calculate the new reinforced profile.
2. Calculate the added / removed / reused materials based on the geometries / layers of point 1.

This work implies the introduction and modification of existing `ReinforcementProfileProtocol` classes, as well as how the builders in the `reinforcement_layers` module function, because they will no longer require to calculate "on the fly" geometries related to added / removed / reused material.