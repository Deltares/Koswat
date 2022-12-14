from typing import Protocol, runtime_checkable

from koswat.io.koswat_reader_protocol import ImportFileObjectModelProtocol


@runtime_checkable
class KoswatShpFomProtocol(ImportFileObjectModelProtocol, Protocol):
    pass