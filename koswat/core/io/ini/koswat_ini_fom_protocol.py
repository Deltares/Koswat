from __future__ import annotations

from configparser import ConfigParser
from typing import Protocol

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class KoswatIniFomProtocol(FileObjectModelProtocol, Protocol):
    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        """
        Imports all the data stored in an dictionary into a `KoswatIniFomProtocol` instance.

        Args:
            ini_config (ConfigParser): Dictionary containing Ini values (section - properties, property - value) to be parsed.

        Returns:
            KoswatIniFomProtocol: Valid instance of a `KoswatIniFomProtocol` with the provided values.
        """
        pass
