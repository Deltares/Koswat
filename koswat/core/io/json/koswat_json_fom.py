from dataclasses import dataclass, field
from typing import Any

from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


@dataclass
class KoswatJsonFom(KoswatJsonFomProtocol):
    file_stem: str = ""
    content: dict[str, Any] = field(default_factory=dict)

    def is_valid(self) -> bool:
        return self.file_stem != "" and self.content is not None
