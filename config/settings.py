#settings: constants, keybinds, theme, config files etc

import pathlib

class Settings:

    def __init__(self) -> None:
        #create path to config file
        #initially hardcode this to ~/.config/journal/journal.conf
        self._configdirectory = pathlib.Path("~/.config/journal").expanduser()
        self._configdirectory.mkdir(parents=True, exist_ok=True)
        self._configfile = self._configdirectory / "journal.conf"
        self._configfile_exist = self._check_if_config_file_exist
        pass

    @property
    def _check_if_config_file_exist(self) -> bool:
        """
        Checks if the config file already exist 
        """
        return self._configfile.is_file()

