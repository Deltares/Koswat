# Dike

In this module we define the Koswat interpretation of a real life Dike and all the associated concepts with it, such as materials or surrounding buildings.

A Koswat dike is mostly represented by an instance of a `KoswatProfileProtocol`. In this object we will contain data structures representing the geometry of the outer profile (`CharacteristicPoints`) and the definition of its inner layers (Grass - Clay - Sand).

## Design decisions.
We describe in `KoswatLayersWrapper` how the profile is defined. The top layers are defined as a `KoswatCoatingLayer` (Grass and Clay) and the `KoswatBaseLayer` is the 'core' (Sand).

Throughout the different sprints the code has changed and potentially some properties / functionality might no longer be required. For instance, I would like to improve the data structure for `KoswatCoatingLayer`:
- Properties:
    - `lower_linestring`: represents the 'ground' coordinates.
    - `upper_points`: represents the 'visible' outter coordinates.
    - `outer_geometry`: represents the profile of the dike __including__ the given layer.
    - `material_geometry`: represents the geometry of the 'KoswatCoatingLayer' without the other layers / core.

- Methods:
    - `get_coated_geometry`: Gets the profile __excluding__ the given layer.
    - `as_data_dict`: It is used by other classes as a subset of properties required to generate new reinforcement profiles. During the _Proof of concept_ this was quite useful, however now it became tedious and ugly.
