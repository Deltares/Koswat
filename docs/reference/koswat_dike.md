# Koswat dike

In this section we will describe how a Koswat dike is defined and what its parts are.

## Koswat properties

A koswat dike is represented by an instance of a `KoswatProfileProtocol`. And its properties represent different aspects of a 'real domain' .

- `input_data`: An implementation of the `KoswatInputProfileProtocol`. This is usually the properties of an already calculated koswat profile based on the given `characteristic_points` and the current scenario the user has created.
- `characteristic_points`: 8 points given by the user describing the dike on (x,y) coordinates, the first four represent the waterside, the last four the polderside.
- `layers_wrapper`: The description on how the layers of the dike are built. Further described in [Dike layers](#dike-layers).
- `location`: coordinate (x, y) where the dike is situated.
- `profile_width`: The difference between the lowest and the highest 'x' coordinates of the profile characteristic points.

## Dike layers
A dike is composed by three layers:

- Sand, the core layer.
- Clay, a coating layer.
- Grass, a (top) coating layer.

These layers are wrapped under a `KoswatLayersWrapperProtocol`  instance. At the same time, each layer is an instance of a `KoswatLayerProtocol` containing the following properties:

- `material_type`: Either Sand, Clay or Grass.
- `upper_points`: The surface points of the layer. This property can be used to calculate the _surface_ ($m^2$) of a material.
- `outer_geometry`: A polygon representing the material layer and the 'wrapped' polygons. For instance, the Clay `outer_geometry` will also include the Sand `material_geometry`.
- `material_geometry`: A closed polygon containing __only__ the points representing the layer.

Using _Image 2. Clay layer highlighted_ as an example, we can map the previous properties:
- `material_type`: Clay, the 'in-between' layer.
- `upper_points`: Line with the 'orange' points, without 'closing' the polygon, something like: [(-18, 0), (0, 5.5), (8, 5.5), (21, 0)].
- `outer_geometry`: Closed geometry using the `upper points` and the 'ground floor' points: [(-18, 0), (0, 5.5), (8, 5.5), (21, 0), __(-18, 0)__].
- `material_geometry`: Closed geometry using the `upper_points` from Clay and the `upper_points` from the layer below (Sand, green points). Should be something like: [(-18, 0), (0, 5.5), (8, 5.5), (21, 0), __(19, 0), (8, 4.75), (0, 4.75), (-14, 0), (-18, 0)__]

|![Base profile sand layer](./imgs/base_profile/base_profile_sand.png)|
|:--:|
|Image 1. Sand layer highlighted|

|![Base profile clay layer](./imgs/base_profile/base_profile_clay.png)|
|:--:|
|Image 2. Clay layer highlighted|

|![Base profile grass layer](./imgs/base_profile/base_profile_grass.png)|
|:--:|
|Image 3. Grass layer highlighted|
