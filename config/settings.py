#settings: constants, keybinds, theme, config files etc

import pathlib

class Settings:

    def __init__(self) -> None:
        #For now the config path is hardcoded to ~/.config/journal/journal.conf
        
        #Create directory- and filepath for the config file
        self._configdirectory = pathlib.Path("~/.config/journal").expanduser()
        self._configdirectory.mkdir(parents=True, exist_ok=True)
        self._configfile = self._configdirectory / "journal.conf"

        #The actual settings are store in a dict:
        #TODO: Need to load standard config into dict, then we can start to
        #check if the file exist or not. If it exist we must replace the 
        #items in the dict with the config dict. If it doesn't exist we must
        #write the dict to the config file. This is to ensure that if the user
        #accidentally removes a line the program doesn't crash.
        self._conf = {
            "save_path" : "~/.journal",
        }
        self._load_or_generate()
        return None

    @property
    def conf(self) -> dict:
        return self._conf

    ### START: Properties for entries in the config

    @property
    def savepath(self) -> str:
        return self._conf["save_path"]

    ### END: Properties for entries in the config

    def _load_or_generate(self) -> None:
        """
        Calls _generate_config_file to create a standard config file if 
        _configfile_exist is false, or calls _load_config_file if it is True
        """
        if self._configfile.is_file():
            self._load_config_file()
        else:
            self._generate_config_file()
        return None

    def _read_config_file(self) -> list:
        """
        Reads the config file and returns the file as a list of strings where
        each line of the config file is an entry in the list
        """
        lines = []
        with self._configfile.open("r") as f:
            line = f.readline()
            while line:
                lines.append(line.strip())
                line = f.readline()
        return lines

    def _clean_comments_from_loaded_file(self, lines: list) -> list:
        """
        Takes a list of lines from the config file and removes lines that
        start with #, e.g. comments
        """
        clean_lines = []
        for line in lines:
            if not(line[0] == "#"):
                clean_lines.append(line)
        return clean_lines

    def _update_conf_with_loaded_file(self, clean_lines: list) -> None:
        """
        Separates the cleaned lines at the equal sign, as key and value, then
        strips it
        """
        for line in clean_lines:
            key, value = line.split("=")
            self._conf.update({key.strip() : value.strip()})
        return None

    def _load_config_file(self) -> None:
        """
        Loads the contents of the config file into a dictionary
        """
        lines = self._read_config_file()
        clean_lines = self._clean_comments_from_loaded_file(lines)
        self._update_conf_with_loaded_file(clean_lines)
        return None

    def _generate_config_file(self) -> None:
        """
        Generates a standardized config file
        """

        self._generated_config_file = [
            "#Set your preferences",
            ]
        for key, value in self._conf.items():
            self._generated_config_file.append(f"{key} = {value}")
        self._write_entry()
        return None

    def _write_entry(self) -> None:
        """
        Writes the generated config file
        """
        with self._configfile.open("w", encoding="utf-8") as f:
            for line in self._generated_config_file:
                f.write(line + "\n")
        return None


