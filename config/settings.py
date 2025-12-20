#settings: constants, keybinds, theme, config files etc

import pathlib

class Settings:

    def __init__(self) -> None:
        #For now the config path is hardcoded to ~/.config/journal/journal.conf
        
        #Create directory- and filepath for the config file
        self._configdirectory = pathlib.Path("~/.config/journal").expanduser()
        self._configdirectory.mkdir(parents=True, exist_ok=True)
        self._configfile = self._configdirectory / "journal.conf"

        #check if file exists
        self._configfile_exist = self._check_if_config_file_exist

        
        pass

    @property
    def _check_if_config_file_exist(self) -> bool:
        """
        Checks if the config file already exist by running is_file from pathlib
        """
        return self._configfile.is_file()

