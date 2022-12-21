# Koswat configuration Input / Output

This module is responsible to define all _FOMs_, _readers_ and _importers_ needed directly or indirectly by a `KoswatRunSettings` instance.

Each module represents a file type and contains the associated instances of `FileObjectModelProtocol` and their related `KoswatReaderProtocol`.

On the root level we find (for now) the importers transforming all the `FileObjectModelProtocol` instances into `KoswatConfigProtocol` ones.