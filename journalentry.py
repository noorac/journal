
from dataclasses import dataclass

@dataclass
class JournalEntry:
    """Creating each journal entry as an object"""
    _filename: str
    _homefolder: str = "/home/noorac/.journal/"

    @property
    def _filepath(self) -> str:
        """Creating the filepath dependant on the config file"""
        return self._homefolder + self._filename

    def create_new_entry(self) -> list[str]:
        """Here we will request the inputs from the user"""
        pass

    def build_new_entry(self) -> str:
        """The data we get from the user is a list, we turn it into a string
        to be saved here"""
        return "".join(self.create_new_entry()) + "\n\n"

    def write_entry(self) -> None:
        """Write the entry to file"""
        #open the file
        self._f = open(self._filepath, "a")
        self._f.write(self.build_new_entry())
        self._f.close()
        return None

    def load_entry(self, sc) -> None:
        self._f = open(self._filepath, "r")
        for x in self._f:
            sc.addstr(x)
        self._f.close()
