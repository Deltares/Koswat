# Calculations

This module contains all classes related to calculation (`ReinforcementProfileCalculationProtocol`) of a Profile (`KoswatProfileProtocol`) resulting in a 'Reinforced' Profile (`ReinforcementProfileProtocol`). 

A calculation should be added into its own module, containing a concrete implementation of `ReinforcementprofileCalculationProtocol` which will return a concrete implementation of `ReinforcementProfileProtocol`. It is also possible that a calculated profile has a new concrete `KoswatInputProfileProtocol`, in which case it will also be included under the same module as the before mentioned.