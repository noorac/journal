#paths: centralize base dirs, filenames

import pathlib

class Path:
    """
    Descr: Creates an object of type pathlib.Path. Used for generating paths
    for reading/writing files
    @param directorypath: str -  Which folder to read/write files
    @param filename: str - Name of the file that is to be written
    """
    def __init__(self, directorypath: str, filename: str) -> None:
        self._path = pathlib.Path(directorypath)
        self._filename = filename
        self._fileextention = ".jrnl"


    @property
    def path(self) -> str:
        """
        @returns the path of the directory
        """
        return self._path.expanduser().as_posix()

    @property
    def savepath(self) -> str:
        """
        @returns the constructed path of directorypath + filename + fileextention
        """
        return (self._path / (self._filename + self._fileextention)).expanduser().as_posix()
