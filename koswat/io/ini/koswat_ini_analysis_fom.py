from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniAnalysisFom(FileObjectModelProtocol):
    dijksectiesSelectie: str
    dijksectieLigging: str
    dijksectieInvoer: str
    scenarioInvoer: str
    eenheidsprijzen: str
    uitvoerfolder: str
    BTW: bool

    def __init__(self) -> None:
        self.dijksectiesSelectie = ""
        self.dijksectieLigging = ""
        self.dijksectieInvoer = ""
        self.scenarioInvoer = ""
        self.eenheidsprijzen = ""
        self.uitvoerfolder = ""
        self.BTW = None

    def is_valid(self) -> bool:
        # TODO add validation
        #        check if values are initialized
        # how to test for an uninitialized bool?
        return (
            (self.dijksectiesSelectie != "")
            & (self.dijksectieLigging != "")
            & (self.dijksectieInvoer != "")
            & (self.scenarioInvoer != "")
            & (self.eenheidsprijzen != "")
            & (self.uitvoerfolder != "")
            & (self.BTW != None)
        )
