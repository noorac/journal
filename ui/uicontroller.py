#uicontroller: event loop, screens, focus, routes keys
import curses
from menu.menu import Menu
from curses.renderer import Renderer

class UIController:
    def __init__(self, stdscr, app):
        self._stdscr = stdscr
        self.app = app
        self.renderer = Renderer(stdscr)
        self.menu = Menu()
        self.title = "Journal"

    def run(self) -> None:
        """
        Main starting point for the whole thing
        """
        cont = True
        while cont:
            cont = self.draw_main_menu()

    def draw_title(self) -> None:
        self.renderer.title(self.title)

    def draw_main_menu(self) -> None:
        self.renderer.menu_lines(self.menu.main_menu)

    def get_ans(self, 

    def main_menu(self) -> bool:
        cont = True
        self.draw_title()
        self.draw_main_menu()

        return cont

    def draw_new_entry(self) -> None:
        pass

    def draw_list_entries(self) -> None:
        pass


    def create_new_entry(self, sc) -> list[str]:
        """Here we will request the inputs from the user"""
        entry_list = []
        key = -1
        #Here is a bunch of mess because of different terminals call enter and 
        #backspace different things. So need to cover bases. Essentially if 
        #enter is pressed, the loop is ended and entry saved, if backspace is 
        #pressed, it backspaces.
        while not ( key == curses.KEY_ENTER or key == 10 or key == 13 or key == "\n"):
            key = sc.getch()
            if key in ["ć", curses.KEY_BACKSPACE]:
                sc.delch()
                entry_list.pop(-1)
            else:
                entry_list.append(chr(key))
        return entry_list




