# Calculations protocols
The following protocols can be found here:

- `ReinforcementInputProfileProtocol`: An extension of `KoswatInputProfileProtocol`.
- `ReinforcementProfileCalculationProtocol`: Extension of the `BuilderProtocol` to define the required calculations that will return the input data required to create a `ReinforcementInputProfileProtocol`.
- `ReinforcementLayerProtocol`: An extension of the `KoswatLayerProtocol` which contains information regarding the new layer geometry, surface as well as the preivous layer geometry.

- `ReinforcementProfileProtocol`: An extension of `KoswatProfileProtocol` which uses `ReinforcementLayersWrapper` instead.
- `ReinforcementProfileBuilderProtocol`: Extension of the `BuilderProtocol` to specify the required data needed to generate a `ReinforcementProfileProtocol`.
