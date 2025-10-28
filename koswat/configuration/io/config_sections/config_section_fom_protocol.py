import abc
from typing import Any

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class ConfigSectionFomProtocol(FileObjectModelProtocol, abc.ABC):
    """
    Protocol for configuration section file object models.
    """

    @classmethod
    @abc.abstractmethod
    def from_config(cls, input_dict: dict[str, Any]) -> "ConfigSectionFomProtocol":
        """
        Create an instance of the class from a dictionary, not setting defaults.

        Args:
            input_dict (dict): Dictionary containing the configuration.

        Returns:
            FileObjectModelProtocol: The created instance.
        """

    @classmethod
    @abc.abstractmethod
    def from_config_set_defaults(
        cls, input_dict: dict[str, Any]
    ) -> "ConfigSectionFomProtocol":
        """
        Create an instance of the class from a dictionary, setting defaults.

        Args:
            input_dict (dict): Dictionary containing the configuration.

        Returns:
            FileObjectModelProtocol: The created instance.
        """

    @abc.abstractmethod
    def merge(self, other: "ConfigSectionFomProtocol") -> "ConfigSectionFomProtocol":
        """
        Merge another ConfigSectionFomProtocol into this one.
        Values from the other instance will overwrite those in this instance
        (only if not empty or default).

        Args:
            other (ConfigSectionFomProtocol): The other instance to merge from.

        Raises:
            TypeError: If the other instance is not of the same type.

        Returns:
            ConfigSectionFomProtocol: The merged instance.
        """
