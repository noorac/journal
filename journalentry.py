
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

    @property
    def _new_entry(self, _entry_list) -> str:
        """Creates a new entry. This will be appended to the self.filename"""
        #_entry_list needs to be fixed, this is the list that comes when you
        #type out a new entry. 
        self._entry_list = []
        # This is a string, and what we will actually append
        self._new_entry = ""
        for idx in range(len(self._entry_list)):
            self._new_entry += self._entry_list[idx]
        self._new_entry += "\n\n"
        return self._new_entry
#open the file
# self._f = open(self._filepath, "a")
# self._f.write(self._entry)
# self._f.close()
# return None

