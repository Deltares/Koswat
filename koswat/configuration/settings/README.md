## Koswat configuration settings.

Contains the Data Object Models used by a `KoswatConfiguration` to understand how a Koswat run will happen.

Ideally we would like both the `FileObjectModel`s and the `DataObjectModel`s to have different definitions and then create a mapper to convert from one to the other. Unfortunately due to time constraints this is at the moment not possible. Therefore the `FileObjectModel`s are also instnaces of the `DataObjectModel`s.