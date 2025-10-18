#UICONTROLLER
import curses
import curses
from renderer.renderer import Renderer


class UIController:
    def __init__(self, stdscr, app):
        self._stdscr = stdscr
        self.r = Renderer(stdscr)
        self.app = app




