from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


@dataclass
class KoswatJsonFom(KoswatJsonFomProtocol):
    file_path: Path = field(default_factory=Path)
    content: dict[str, Any] = field(default_factory=dict)

    @property
    def file_stem(self) -> str:
        return self.file_path.stem

    def is_valid(self) -> bool:
        return self.file_stem and self.content
