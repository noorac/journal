from dataclasses import dataclass

@dataclass
class JournalEntry:
    """Creating each journal entry as an object"""
    filename : str = filename
    homefolder: str = "/home/noorac/.journal/"

    @property
    def filepath(self) -> str:
        return homefolder + filename

