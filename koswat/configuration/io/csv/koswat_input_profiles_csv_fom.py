from typing import List

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class KoswatInputProfilesCsvFom(FileObjectModelProtocol):
    input_profile_fom_list: List[dict]

    def __init__(self) -> None:
        self.input_profile_fom_list = []

    def is_valid(self) -> bool:
        return self.input_profile_fom_list and any(self.input_profile_fom_list)
