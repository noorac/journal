#Random utility functions

def load_entry(filepath: str) -> str:
    """Takes a filepath as argument, opens the file at that path for reading, 
        and returns the content/entry as one long string"""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
