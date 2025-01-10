from typing import Protocol, runtime_checkable

from koswat.core.protocols.data_object_model_protocol import DataObjectModelProtocol


@runtime_checkable
class KoswatConfigProtocol(DataObjectModelProtocol, Protocol):
    def is_valid(self) -> bool:
        """
        Validates the current `KoswatConfigProtocol` instance.

        Returns:
            bool: `True` when the current instance is valid to be used as a configuration class.
        """
        pass
