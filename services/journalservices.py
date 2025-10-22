#journalservices: file I/O, listing, today-name, etc.

import pathlib

from models import journalentry


class JournalService:
    """
    Keeps track of the .journal directory, writing and reading to file.
    Generates JournalEntries
    """
    def __init__(self, journaldirectory: str) -> None:
        self._journaldirectory = pathlib.Path(journaldirectory).expanduser()
        self._list_of_entries = self.update_directories()

    @property
    def journaldirectory(self) -> str:
        """
        Returns the journaldirectory as a string
        """
        return self._journaldirectory.as_posix()

    def update_directories(self) -> None:
        """
        Traverses the directory set in .config(currently hardcoded to be
        "~/.journal") and creates a list of posix-objects for each file in the
        directory. This list is then contained in the self._list_of_entries
        var.
        """
        self._list_of_entries = [x for x in self._journaldirectory.iterdir()]
        return None

    def _build_path(self, name) -> pathlib.Path:
        """
        Builds a path at journaldirectory + name
        """
        return self._journaldirectory / name

    def new_entry(self, name: str) -> journalentry.JournalEntry:
        """
        Generates a new JournalEntry object with _filename = name and
        _filepath = PosixPath object.
        """
        return journalentry.JournalEntry(_filename = name, _homefolder = self._build_path(name))


    def write_entry(self, journalentry) -> None:
        """
        Takes a JournalEntry object and writes that object to file
        """
        with journalentry.path.open("a", encoding="utf-8") as f:
            f.write(journalentry.entry)
            f.write("\n\n")
        self.update_directories()
        return None

    def read_entry(self, journalentry) -> str:
        """
        Takes a journalentry object and tries to open and read the content
        of the object.
        """
        entry = journalentry.path.read_text
        with journalentry.path("r", encoding="utf-8") as f:
            f.read
        return
