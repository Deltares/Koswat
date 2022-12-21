# IO

This module is intended for general Input / Output operations and readers / writers.
Concrete readers / writers and FileObjectModels should not be placed here but under a concrete io module within the corresponding class.

## File Object Model
In koswat we consider a `File Object Model` (FOM) a class representation of an actual file. This class will contain whenever possible a 1:1 reflection from said file and will do mapping of direct types. For instance, mapping into simple types such as `int`, `float`, `str` or `pathlib.Path`. However, it will not be responsible for mapping a value which implies importing another file.

## Reader
We define a reader as a class responsible of opening an input file stream and converting its content into a [FOM](#file-object-model).

## Importer
We define an importer as a class responsible of translating the contents of a file into a `Domain Object Model`  (DOM).

An importer can use one (or many) [readers](#reader) to achieve such transformation as well as other importers or builders (`BuilderProtocol`)

## Writer
We define a writer as a class responsible to open an output file stream and dump a [FOM](#file-object-model) content in it.

## Exporter
We define an exporter as a class responsible of translating a `Domain Object Model` (DOM) into a newly created file.

An exporter can use as many [writers](#writer) as required.
