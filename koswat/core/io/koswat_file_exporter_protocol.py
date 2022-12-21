from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from koswat.core.io.file_object_model_protocol import ExportFileObjectModelProtocol
from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.core.protocols import BuilderProtocol


@runtime_checkable
class KoswatFileExporterProtocol(KoswatExporterProtocol, BuilderProtocol, Protocol):
    data_object_model: Any
    export_filepath: Path

    def build(self) -> ExportFileObjectModelProtocol:
        """
        Builds a concrete `ExportFileObjectModelProtocol` based on the `data_object_model`.

        Returns:
            ExportFileObjectModelProtocol: Instance represented as the target file type.
        """
        pass

    def export(self, file_object_model: ExportFileObjectModelProtocol) -> None:
        """
        Exports the given `file_object_model` into a concrete file format.

        Args:
            file_object_model (ExportFileObjectModelProtocol): File object model containing data to be written.
        """
        pass
