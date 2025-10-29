from typing import Any, Protocol, runtime_checkable

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@runtime_checkable
class ConfigSectionFomProtocol(FileObjectModelProtocol, Protocol):
    """
    Protocol for configuration section file object models.
    """

    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any], set_defaults: bool
    ) -> "ConfigSectionFomProtocol":
        """
        Create an instance of the class from a dictionary, not setting defaults.

        Args:
            input_dict (dict): Dictionary containing the configuration.

        Returns:
            FileObjectModelProtocol: The created instance.
        """
