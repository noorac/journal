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
        self._journaldirectory.mkdir(parents=True, exist_ok=True)
        self._update_directories()

    @property
    def journaldirectory(self) -> str:
        """
        Returns the location where the journals are saved as a string
        """
        return self._journaldirectory.as_posix()

    @property
    def list_of_entries(self) -> list[str]:
        """
        Returns a list containing the names of all the files in 
        journaldirectory as strings
        """
        return [x.stem for x in self._list_of_entries]

    def _update_directories(self) -> None:
        """
        Traverses the directory set in .config(currently hardcoded to be
        "~/.journal") and creates a list of posix-objects for each file in the
        directory. This list is then contained in the self._list_of_entries
        var.
        """
        self._list_of_entries = [x for x in self._journaldirectory.iterdir()]

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
        return journalentry.JournalEntry(filepath = self._build_path(name))


    def write_entry(self, journalentry, entry_text) -> None:
        """
        Takes a JournalEntry object and a list of chars and writes 
        that list at the location of the object 
        """
        with journalentry.path.open("a", encoding="utf-8") as f:
            f.write(entry_text)
            f.write("\n\n")
        self._update_directories()
        return None

    def read_entry(self, journalentry) -> str:
        """
        Takes a journalentry object and tries to open and read the content
        of the object.
        """
        if journalentry.filepath.is_file():
            return journalentry.path.read_text
        else:
            return "File doesn't exist"
        
