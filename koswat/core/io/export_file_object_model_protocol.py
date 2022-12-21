from typing import Any, List, Protocol, runtime_checkable

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@runtime_checkable
class ExportFileObjectModelProtocol(FileObjectModelProtocol, Protocol):
    def get_lines(self) -> List[Any]:
        """
        Returns all the data from this `ExportFileObjectModelProtocol` as lines.
        Generally used for export functionality.

        Returns:
            List[Any]: Data ordered in lines
        """
        pass
