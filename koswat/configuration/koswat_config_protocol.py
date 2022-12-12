from typing import Protocol


class KoswatConfigProtocol(Protocol):
    def is_valid(self) -> bool:
        """
        Validates the current `KoswatConfigProtocol` instance.

        Returns:
            bool: `True` when the current instance is valid to be used as a configuration class.
        """
        pass