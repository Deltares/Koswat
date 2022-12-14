## Koswat.Configuration.Converters

This module contains the mapping of a setting `FileObjectModel` (`FOM`) into its corresponding `DataObjectModel` (`DOM`).

### Why using these build patterns instead of inheritance `FOM` -> `DOM` ?

Mostly because I want to reduce logic in the classes and some of the `FOM` do not directly translate into a `DOM`. Some `DOM` settings require the combination of different `FOM` settings in order to make sense. 