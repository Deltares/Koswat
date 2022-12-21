import configparser
from pathlib import Path
from typing import Type

from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.core.io.txt.koswat_txt_fom_protocol import KoswatTxtFomProtocol


class KoswatTxtReader(KoswatReaderProtocol):

    koswat_txt_fom_type: Type[KoswatTxtFomProtocol]

    def __init__(self) -> None:
        self.koswat_txt_fom_type = None

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix.lower() == ".txt"

    def read(self, file_path: Path) -> KoswatTxtFomProtocol:
        if not self.supports_file(file_path):
            raise ValueError("Txt file should be provided")
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        if not self.koswat_txt_fom_type:
            raise ValueError("KoswatTxtFom type needs to be specified.")

        return self.koswat_txt_fom_type.from_text(file_path.read_text())
