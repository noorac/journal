#journalentry: the journal entries themselves

import curses
import pathlib
from dataclasses import dataclass

@dataclass
class JournalEntry:
    """Creating each journal entry as an object"""
    _filename: str
    _filepath: pathlib.Path

    @property
    def title(self) -> str:
        """Returns the filename, i.e. the title of the entry"""
        return self._filename

    @property
    def filepath(self) -> str:
        """Creating the filepath dependant on the config file"""
        return self._filepath.as_posix()

    def create_new_entry(self, sc) -> list[str]:
        """Here we will request the inputs from the user"""
        entry_list = []
        key = -1
        #Here is a bunch of mess because of different terminals call enter and 
        #backspace different things. So need to cover bases. Essentially if 
        #enter is pressed, the loop is ended and entry saved, if backspace is 
        #pressed, it backspaces.
        while not ( key == curses.KEY_ENTER or key == 10 or key == 13 or key == "\n"):
            key = sc.getch()
            if key in ["ć", curses.KEY_BACKSPACE]:
                sc.delch()
                entry_list.pop(-1)
            else:
                entry_list.append(chr(key))
        return entry_list

    def build_new_entry(self, sc) -> str:
        """The data we get from the user is a list, we turn it into a string
        to be saved here"""
        return "".join(self.create_new_entry(sc)) + "\n\n"

    def write_entry(self, sc) -> None:
        """Write the entry to file"""
        #open the file
        self._f = open(self._filepath, "a")
        self._f.write(self.build_new_entry(sc))
        self._f.close()
        return None

