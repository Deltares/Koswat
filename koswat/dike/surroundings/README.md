# Surroundings

This module aims to contain all classes that represent the surroundings of a dike (or list of them).

A "surrounding" is defined by the `KoswatSurroundingsProtocol`. It contains a list of points (`PointSurroundingsProtocol`) which represent locations (`PointSurroundingsProtocol.location`) in a dike traject.
We mainly distinguish two types of surroundings:

- Obstacles (`SurroundingsObstacle`): they cannot be repaired or replaced (removed and built again), becoming a boundary for a `ReinforcementProfile` and therefore limiting which type of reinforcements can be applied at a given location (`PointSurroundingsProtocol`).
- Infrastructures (`SurroundingsInfrastructure`), they can be both reworked and / or replaced (removed and built again). When a `ReinforcementProfile` at a given location (`PointSurroundingsProtocol`) has infrastructures in their `surroundings_matrix` then we use them to estimate additional costs depending on whether they will be reworked or replaced.

These surroundings are clustered in a `SurroundingsWrapper` class which can be built through the `SurroundingsWrapperBuilder` by providing the file representations of the surroundings (`.csv` file) and the dike traject locations (`.shp` file). This wrapper can retrieve the information related to all wrapped surroundings that are to be applied for a given scenario.

A simple UML class diagram representing the relationships:

|![Koswat surroundings in the code](../../../docs/reference/imgs/surroundings_diagram.drawio.png)|
|:--:|
|Image 1. Surroundings code-wise|