#journalservices: file I/O, listing, today-name, etc.

import pathlib


class JournalService:
    """
    Keeps track of the files in the savepath.
    
    """
    def __init__(self, journaldirectory) -> None:
        self._journaldirectory = pathlib.Path(journaldirectory).expanduser()
        self._list_of_entries = self.update_directories()

    def update_directories(self) -> None:
        """
        Traverses the directory set in .config(currently hardcoded to be
        "~/.journal") and creates a list of posix-objects for each file in the
        directory. This list is then contained in the self._list_of_entries
        var.
        """
        self._list_of_entries = [x for x in self._journaldirectory.iterdir()]
        return None

    def write_entry(self, journalentry) -> None:
        """
        Takes a JournalEntry object and writes that object to file
        """
        with self._journalentry.path.open("a", encoding="utf-8") as f:
            f.write(self._journalentry.entry)
            f.write("\n\n")
        return None
