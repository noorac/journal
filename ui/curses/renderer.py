#renderer: draw helpers: boxes, split panes, input
import curses
import time

class Renderer:
    def __init__(self, stdscr) -> None:
        self._stdscr = stdscr
        self.refresh_geometry()
        curses.use_default_colors();
        self.create_color_pairs()

    #PROPERTIES

    @property
    def h(self) -> int:
        """Returns the height"""
        return self._h

    @property
    def w(self) -> int:
        """Returns the width"""
        return self._w

    #METHODS

    def clear(self) -> None:
        """Clear the screen"""
        self._stdscr.clear()

    def refresh(self) -> None:
        """Redraws the screen"""
        self._stdscr.refresh()

    def create_color_pairs(self) -> None:
        """Generates curses color pairs
        @pair 1: fg=black, bg=red
        """
        curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_RED)

    def refresh_geometry(self) -> None:
        """Refreshes the h / w values"""
        self._h, self._w = self._stdscr.getmaxyx()

    def title(self, text: str) -> None:
        """Draws the title
        @param text: the title to draw
        """
        self.refresh_geometry()
        y = 1
        x = (self.w // 2) - (len(text) // 2)
        self._stdscr.addstr(y, max(0, x), text, curses.color_pair(1))

    def get_key(self, x, y) -> str:
        """
        TODO: Not sure if this should return str or object or something else
        """
        return self._stdscr.getkey(x,y)

    def menu_lines(self, lines: list[str], 
                   start_y: int = 3, start_x: int = 1) -> None:
        """Prints out the menulines
        @param lines list[str]: list of menu options
        @param start_y int: what line y should start
        @param start_x int: what character x should start
        """
        for i, line in enumerate(lines):
            self._stdscr.addstr(start_y + i, start_x, line)

    def prompt(self, y: int, x: int, prompt_text: str) -> None:
        """Called to make a prompt to screen
        @param y int: what line y should the prompt be on
        @param x int: what character x should the prompt be on
        @param prompt_text str: the text of the prompt
        """
        self._stdscr.addstr(y, x, prompt_text)

    def message_centered(self, text: str, pause_ms: int = 750) -> None:
        """Send a message to the center of the screen for a certain amount
            of time.
        @param text str: the text to be printed
        @param pause_ms int: the amount of time in ms(default 750)
        """
        self._stdscr.clear()
        self.refresh_geometry()
        y = 1
        x = (self.w // 2) - (len(text) // 2)
        self._stdscr.addstr(y, max(0, x), text)
        self._stdscr.refresh()
        time.sleep(pause_ms / 1000)
