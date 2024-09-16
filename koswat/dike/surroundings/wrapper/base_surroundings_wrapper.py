from abc import ABC, abstractmethod

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)


class BaseSurroundingsWrapper(ABC):
    @property
    def _surroundings_collection(self) -> dict[str, KoswatSurroundingsProtocol]:
        """
        The collection of `KoswatSurroundingsProtocol` objects that are considered for a scenario analysis.

        Returns:
            list[KoswatSurroundingsProtocol]: Collection of surroundings to include in analysis.
        """
        _surroundings = {
            _prop: _value
            for _prop, _value in self.__dict__.items()
            if isinstance(_value, KoswatSurroundingsProtocol)
        }

        return self._exclude_surroundings(_surroundings)

    @abstractmethod
    def _exclude_surroundings(self, surroundings_dict: dict) -> dict:
        """
        Method to exclude surroundings depending on the concrete class.

        Args:
            surroundings_dict (dict): Dictionary of surroundings that requires filtering.

        Raises:
            NotImplementedError: When no concrete class is implementing it.

        Returns:
            dict: Filtered dictionary.
        """
        raise NotImplementedError("Should be implemented in concrete class")
