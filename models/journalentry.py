#journalentry: the journal entries themselves


class JournalEntry:
    """Creating each journal entry as an object"""
    def __init__(self, filepath) -> None:
        self._filepath = filepath

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

