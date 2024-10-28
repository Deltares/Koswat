from abc import ABC

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)


class BaseSurroundingsWrapper(ABC):
    @property
    def surroundings_collection(self) -> dict[str, KoswatSurroundingsProtocol]:
        """
        The collection of `KoswatSurroundingsProtocol` objects that are considered for a scenario analysis.

        Returns:
            list[KoswatSurroundingsProtocol]: Collection of surroundings to include in analysis.
        """
        return {
            _prop: _value
            for _prop, _value in self.__dict__.items()
            if isinstance(_value, KoswatSurroundingsProtocol)
        }
