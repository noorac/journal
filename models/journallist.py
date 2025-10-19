#journallist: holds journalentry objects
from dataclasses import dataclass, field
from typing import List, Iterator

import journalentry

@dataclass
class JournalList:
    entries: List[journalentry.JournalEntry] = field(default_factory=list)

    def add_entry(self, entry: journalentry.JournalEntry) -> None:
        """Adds an entry of JournalEntry"""
        self.entries.append(entry)

    def __len__(self) -> int:
        """If calling len on JournalList return the length of entries list"""
        return len(self.entries)

    def __getitem__(self, idx: int) -> journalentry.JournalEntry:
        """If subscripting the JournalList like JournalList[i], __getitem__ is 
        called and the i will return entries[i]"""
        return self.entries[idx]

    def __iter__(self) -> Iterator[journalentry.JournalEntry]:
        """Allows us to iterate over JournalList e.g. for x in JournalList, and 
        this will then let x be each entry in entries"""
        return iter(self.entries)


