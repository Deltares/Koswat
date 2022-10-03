## v0.3.0 (2022-10-03)

### Feat

- **CharacteristicPoints**: Created characteristic points to replace the previous 'ProtocolSide' related classes. Introduced builder to allow initial or reinforced profile creation
- **KoswatLayersBuilder**: We now can create layers based on the provided depth
- **ProfileReinforcementCostBuilder**: Generates a cost report for the new profile based on the extra required volume
- **KoswatReport**: Added KoswatReport to generate costs overviews
- It is now possible to create layers from a dictionary
- **koswat_layers;koswat_profile_builder**: Added new class to represent the layers of a profile, their material and so on.
- **koswat/calculations**: Added profile reinforcement calculation
- **koswat/profiles**: Added koswat profiles and related properties. They can now be built from an input profile

## v0.2.0 (2022-09-27)

### Feat

- **koswat**: Initial commit. Created Initial architecture and basic tests for the structure given. Added version control through commitizen
