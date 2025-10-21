from dataclasses import dataclass, field

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@dataclass
class KoswatInputProfileJsonFom(FileObjectModelProtocol):
    input_profile_fom: dict[str, str | float] = field(default_factory=dict)

    def is_valid(self) -> bool:
        return self.input_profile_fom
