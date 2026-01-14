#journalentry: the journal entries themselves


class JournalEntry:
    """Creating each journal entry as an object"""
    def __init__(self, filepath) -> None:
        self._filepath = filepath
        self._entry = []

    @property
    def title(self) -> str:
        """
        Returns the filename as a string
        """
        return self._filepath.stem

    @property
    def filepath_str(self) -> str:
        """
        Returns the full path of the file as a string
        """
        return self._filepath.as_posix()

    @property
    def filepath(self) -> str:
        """
        Returns the full path of the file as a string
        """
        return self._filepath

    @property
    def entry(self) -> list:
        """
        Returns the list of characters that is the entry for the object
        """
        return self._entry

    # METHODS

    def load_entry(self) -> None:
        """
        This is called by journalservice if a file exist with the name of today
        and this method will then take pathlib.read_text() from that file and
        put it into self._entry. 
        """
        self._entry[:] = self._filepath.read_text()
        return None

    def no_entry(self) -> None:
        """
        Dummy function to return nothing
        """
        return None

    def as_str(self) -> str:
        """
        Returns a joined string version of self._entry
        """
        return "".join(self._entry)

    def append(self, key: int) -> None:
        """
        Adds a character to self._entry
        """
        self._entry.append(chr(key))
        return None

    def pop(self) -> None:
        """
        Removes the last element of self._entry
        """
        self._entry.pop(-1)
        return None
