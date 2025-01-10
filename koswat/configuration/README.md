# Configuration

Represents all settings related to the data required by `Koswat` to generate a `KoswatSummary`, this includes the definition of an initial `KoswatProfile`, the `KoswatScenario`s etc.

A `KoswatConfigurationProtocol` is a concrete definition of a `DataObjectModelProtocol`.

## Design decisions. 
Because not all files can be imported 1:1 it is important to remind of how Koswat import functionality is thought:
- A __file__ is __read__ into a __FOM__ and __built__ into a __DOM__
- `File` -> `KoswatReaderProtocol` -> `FileObjectModelProtocol` -> `BuilderProtocol` -> `DataObjectModelProtocol`
- `File` -> `KoswatImporterProtocol` -> `DOM`

This implies that a `KoswatImporterProtocol` will be responsible of providing a `DataObjectModelProtocol`. Inside the instance of the `KoswatImporterProtocol` other importers can also take place. Either way, an importer will ensure that the correct `FileReaderProtocol` is selected to get the `FileObjectModel` from a `File` and together with any other related data transformed into said `DOM` by using an instance of a `BuilderProtocol`.