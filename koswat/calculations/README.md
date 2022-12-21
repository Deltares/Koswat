# Calculations

This module contains the information on calculating a reinforcement (`ReinforcementProfileCalculationProtocol`) for a Profile (`KoswatProfileProtocol`) resulting in a 'Reinforced' Profile (`ReinforcementProfileProtocol`). It is divided in submodules representing the different types of reinforcements and their builders.

The module is divided as:
- __io__: Input / output module containing the concrete importers and exporters for the models here defined.
- __outside_slope_reinforcement__: Module containing the definition of all `OutsideSlopeReinforcementProfile` implementations.
- __standard_reinforcement__: Module containing the definition of all `StandardReinforcementProfile` implementations.
- __protocols__: Module where the `typing.Protocol` concrete definitions used across the whole calculation modules are saved.

At  the same time we expose directly the 
- `ReinforcementLayersWrapper`: Concrete implementation of `KoswatLayersWrapperProtocol` which uses `ReinforcementBaseLayer` and `ReinforcementCoatingLayer` instead (both from instances of `ReinforcementLayerProtocol`).
- `ReinforcementProfileBuilderFactory`: Factory to retrieve the correct instances of a `ReinforcementProfileBuilderProtocol`.

## Design decisions.
It could be argued that some of the code could be reduced by using abstractions or simple inheritance. However I opted for 'duplicating' methods logic in order to reduce the dependency between classes thus making them totally independent. Alas the usage of protocols over abstractions.

A reinforcement calculation will naturally be found in its respective `*_profile_calculation.py` file. This way we isolate the logic to get each one of the values that compose a specific reinforcement profile, allowing us for better maintainability and verification.