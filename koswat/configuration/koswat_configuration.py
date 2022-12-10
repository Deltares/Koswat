class KoswatConfiguration:
    def is_valid(self) -> bool:
        raise NotImplementedError()

    def run(self) -> None:
        if not self.is_valid():
            return
