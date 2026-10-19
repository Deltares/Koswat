from abc import ABC, abstractmethod


class RoadClassBase(ABC):
    @property
    @abstractmethod
    def key(self) -> str:
        raise NotImplementedError("Subclasses must implement the 'key' property.")

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other) -> bool:
        if not isinstance(other, RoadClassBase):
            return False
        return self.key == other.key
