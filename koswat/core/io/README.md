# IO

This module is intended for general Input / Output operations and readers / writers.
Concrete readers / writers and FileObjectModels should not be placed here but under a concrete io module within the corresponding class.

## Design decisions. 

### Input
- A __file__ is __read__ into a __FOM__ and __built__ into a __DOM__
- `File` -> `KoswatReaderProtocol` -> `FileObjectModelProtocol` -> `BuilderProtocol` -> `DataObjectModelProtocol`
- `File` -> `KoswatImporterProtocol` -> `DataObjectModelProtocol`

### Output
- A __DOM__ is __built__ into a __FOM__ and __written__ in a __file__
- `DataObjectModelProtocol` -> `KoswatWriterProtocol` -> `FileObjectModelProtocol` -> `BuilderProtocol` -> `File`
- `DataObjectModelProtocol` -> `KoswatExporterProtocol` -> `File`

## File Object Model
In koswat we consider a `FileObjectModelProtocol` (FOM) a class representation of an actual file. This class will contain whenever possible a 1:1 reflection from said file and will do mapping of direct types. For instance, mapping into simple types such as `int`, `float`, `str` or `pathlib.Path`. However, it will not be responsible for mapping a value which implies importing another file.

## Data Object Model
In koswat a `DataObjectModelProtocol` (DOM) is a class that represents a software data structure or object required within the Koswat domain in `Python` language.

__Important:__ Not all objects in Koswat are required to be a DOM.

## Builder
We consider a `BuilderProtocol` (builder) a class which works as a pipeline transition between a [FOM](#file-object-model) and a [DOM](#data-object-model) in either direction.

## Reader
We define a `KoswatReaderProtocol` (reader) as a class responsible of opening an input file stream and converting its content into a [FOM](#file-object-model).

## Importer
We define a `KoswatImporterProtocol` (importer) as a class responsible of translating the contents of a file into a [DOM](#data-object-model).

An importer can use one (or many) [readers](#reader) to achieve such transformation as well as other importers or builders (`BuilderProtocol`)

## Writer
We define a `KoswatWriterProtocol` (writer) as a class responsible to open an output file stream and dump a [FOM](#file-object-model) content in it.

## Exporter
We define a `KoswatExporterProtocol` (exporter) as a class responsible of translating a [DOM](#data-object-model) into a newly created file.

An exporter can use as many [writers](#writer) and [builders](#builder) as required.
