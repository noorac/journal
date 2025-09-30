
from dataclasses import dataclass

@dataclass
class JournalEntry:
    """Creating each journal entry as an object"""
    filename: str
    homefolder: str = "/home/noorac/.journal/"

    @property
    def filepath(self) -> str:
        """Creating the filepath dependant on the config file"""
        return self.homefolder + self.filename

