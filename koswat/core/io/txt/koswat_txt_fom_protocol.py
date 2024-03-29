from __future__ import annotations

from typing import Protocol

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class KoswatTxtFomProtocol(FileObjectModelProtocol, Protocol):
    @classmethod
    def from_text(cls, file_text: str) -> KoswatTxtFomProtocol:
        """
        Imports all the data stored in text form.

        Args:
            file_text (str): Raw data in string format.

        Returns:
            KoswatTxtFomProtocol: Valid instance of a `KoswatTxtFomProtocol` with the provided values.
        """
        pass
