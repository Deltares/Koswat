# Calculations

This module contains the information on calculating a reinforcement (`ReinforcementProfileCalculationProtocol`) for a Profile (`KoswatProfileProtocol`) resulting in a 'Reinforced' Profile (`ReinforcementProfileProtocol`). It is divided in submodules representing the different types of reinforcements and their builders.

At the root of this module we define the generic protocols:
- `ReinforcementInputProfileProtocol`: An extension of `KoswatInputProfileProtocol`.
- `ReinforcementProfileCalculationProtocol`: Extension of the `BuilderProtocol` to define the required calculations that will return the input data required to create a `ReinforcementInputProfileProtocol`.
- `ReinforcementLayerProtocol`: An extension of the `KoswatLayerProtocol` which contains information regarding the new layer geometry, surface as well as the preivous layer geometry.
- `ReinforcementLayersWrapper`: Concrete implementation of `KoswatLayersWrapperProtocol` which uses `ReinforcementBaseLayer` and `ReinforcementCoatingLayer` instead (both from instances of `ReinforcementLayerProtocol`).
- `ReinforcementProfileProtocol`: An extension of `KoswatProfileProtocol` which uses `ReinforcementLayersWrapper` instead.
- `ReinforcementProfileBuilderProtocol`: Extension of the `BuilderProtocol` to specify the required data needed to generate a `ReinforcementProfileProtocol`.
- `ReinforcementProfileBuilderFactory`: Factory to retrieve the correct instances of a `ReinforcementProfileBuilderProtocol`.

