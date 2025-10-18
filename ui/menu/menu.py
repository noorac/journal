from dataclasses import dataclass

@dataclass
class Menu:

    @property
    def main_menu(self) -> list:
        """Returns the main menu"""
        return ["E) Press enter for new entry",
                "l) Press l for list",
                "q) press q to quit",
                ]

