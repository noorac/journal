#UICONTROLLER
import curses
from menu.menu import Menu
from renderer.renderer import Renderer

class UIController:
    def __init__(self, stdscr, app):
        self._stdscr = stdscr
        self.app = app
        self.r = Renderer(stdscr)
        self.m = Menu()

    #Methods
    def draw_menu(self) -> None:
        self.r.menu_lines(self.m.main_menu)





