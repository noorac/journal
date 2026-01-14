#renderer: draw helpers: boxes, split panes, input
import curses
import time

class Renderer:
    def __init__(self, win) -> None:
        self._win = win
        self.refresh_geometry()
        curses.use_default_colors();
        self.create_color_pairs()

    #PROPERTIES

    @property
    def max_h(self) -> int:
        """Returns the max height of the window"""
        return self._max_h

    @property
    def max_w(self) -> int:
        """Returns the max width of the window"""
        return self._max_w

    @property
    def ypos(self) -> int:
        """
        Returns the y position of the cursor
        """
        return self._win.getyx()[0]

    @property
    def xpos(self) -> int:
        """
        Returns the x position of the cursor
        """
        return self._win.getyx()[1]

    #METHODS

    def __getattr__(self, name):
        """
        Called when attribute isn't found on Renderer
        """
        return getattr(self._win, name)

    def create_color_pairs(self) -> None:
        """Generates curses color pairs using following logic:
        @pair 1: fg=black, bg=red
        """
        curses.init_pair(1,curses.COLOR_MAGENTA,-1)

    def refresh_geometry(self) -> None:
        """Refreshes the heigth and width values of the window by calling
        getmaxyx on win
        """
        self._max_h, self._max_w = self._win.getmaxyx()

    def title(self, text: str) -> None:
        """Draws the title
        @param text: the string of text to draw as the title
        """
        self.refresh_geometry()
        y = 0
        x = (self.max_w // 2) - (len(text) // 2)
        
        #Hardcoded attributes:
        attr = curses.color_pair(1) | curses.A_UNDERLINE | curses.A_BOLD

        self._win.addstr(y, max(0, x), text, attr)
        self._win.refresh()


    def get_multi_key(self, y, x) -> str:
        """
        Does the same as get_key, however, also turns on echo, and then turns
        it off again. This method needs updates/fixes
        """
        curses.echo()
        try:
            inputstr = self._win.getstr(y, x)
        finally:
            curses.noecho()
        try:
            return inputstr.decode("utf-8", errors="ignore")
        #TODO: FIX EXCEPTION
        except Exception:
            return ""
            return self._win.getkey(y, x)

    def menu_lines(self, lines: list[str], 
                   start_y: int = 3, start_x: int = 1) -> None:
        """Prints out the menulines you send to it:
        @param lines list[str]: list of menu options
        @param start_y int: what line y should start
        @param start_x int: what character x should start
        """
        for i, line in enumerate(lines):
            self._win.addstr(start_y + i, start_x, line)

    # def prompt(self, y: int, x: int, prompt_text: str) -> None:
    #     """Called to make a prompt to screen
    #     @param y int: what line y should the prompt be on
    #     @param x int: what character x should the prompt be on
    #     @param prompt_text str: the text of the prompt
    #     """
    #     self._win.addstr(y, x, prompt_text)


    def message_centered(self, text: str, pause_ms: int = 750) -> None:
        """Send a message to the center of the screen for a certain amount
            of time. 
        @param text str: the text to be printed
        @param pause_ms int: the amount of time in ms(default 750)
        """
        self._win.clear()
        self.refresh_geometry()
        y = 1
        x = (self.max_w // 2) - (len(text) // 2)
        self._win.addstr(y, max(0, x), text)
        self._win.refresh()
        time.sleep(pause_ms / 1000)

