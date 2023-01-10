# Koswat dike

In this section we will describe how a Koswat dike is defined and what its parts are.

## Koswat properties
A dike is composed by three layers:

- Sand, the core layer.
- Clay, a coating layer.
- Grass, a (top) coating layer.

These layers are wrapped under a `KoswatLayersWrapperProtocol`  instance. At the same time, each layer is an instance of a `KoswatLayerProtocol` containing the following properties:

- `material_type`: Either Sand, Clay or Grass.
- `upper_points`: The surface points of the layer. I
- `outer_geometry`: A polygon representing the material layer and the 'wrapped' polygons. For instance, the Clay `outer_geometry` will also include the Sand `material_geometry`.
- `material_geometry`: A closed polygon containing __only__ the points representing the layer.

Using _Image 1_ as an example, we can map the previous properties:
- `material_type`: Clay, the 'in-between' layer.
- `upper_points`: Line with the 'orange' points, without 'closing' the polygon, something like: [(-18, 0), (0, 5.5), (8, 5.5), (21, 0)].
- `outer_geometry`: Closed geometry using the `upper points` and the 'ground floor' points: [(-18, 0), (0, 5.5), (8, 5.5), (21, 0), __(-18, 0)__].
- `material_geometry`: Closed geometry using the `upper_points` from Clay and the `upper_points` from the layer below (Sand, green points). Should be something like: [(-18, 0), (0, 5.5), (8, 5.5), (21, 0), __(19, 0), (8, 4.75), (0, 4.75), (-14, 0), (-18, 0)__]

|![Base profile clay layer](./imgs/base_profile/base_profile_clay.png)|
|:--:|
|Image 1. Clay layer highlighted|

## Reinforced profile