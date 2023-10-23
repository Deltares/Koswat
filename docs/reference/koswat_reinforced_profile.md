# Reinforcement profile

In koswat we consider a reinforcement profile the result of applying one of the multiple possible reinforcement calculations on an instance of a `KoswatProfileBase` ([Koswat dike](koswat_dike.md)).

This chapter covers the description of a reinforcement profile and its parts.

## Properties

A reinforcement profile implements the `ReinforcementProfileProtocol`, which is a specialization of the `KoswatProfileProtocol` with some differences:

- `input_data`: Similar to the base profile `input_data` but instead implements the `ReinforcementInputProfileProtocol`, a specialization of the (`KoswatInputProfileProtocol`) which depends on the type of [reinforcement](#possible-reinforcements) being applied.
- `old_profile`: New property which contains the [koswat profile](koswat_dike.md#koswat-dike) from which the calculation was based on.


## Possible reinforcements.

We have two main different sort of reinfocements which contain also subtypes for said reinforcements: 

- __Outside slope reinforcement__: Cofferdam (_kistdam_), based on the `OutsideSlopeReinforcementProfile`.
- __Standard reinforcement__: Piping wall (_kwelscherm_), soil (_grondmaatregel profiel_), stability wall (_stabiliteitswand_). The previous being based on the `StandardReinforcementProfile`.

In addition, the above mentioned reinforcements can also implement their own `ReinforcementInputProfileProtocol`, which are after all extensions of the `KoswatInputProfileBase` with extra properties.