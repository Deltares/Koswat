from typing import Protocol, runtime_checkable

from koswat.core.io.koswat_reader_protocol import ImportFileObjectModelProtocol


@runtime_checkable
class KoswatCsvFomProtocol(ImportFileObjectModelProtocol, Protocol):
    pass
