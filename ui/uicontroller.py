#uicontroller: event loop, screens, focus, routes keys
import curses
from models import journalentry
from models.journalentry import JournalEntry
from ui.menu.menu import Menu
from ui.curses.renderer import Renderer
import utils.date_utils

class UIController:
    def __init__(self, stdscr, app):
        self._stdscr = stdscr
        self.app = app
        self.create_windows()
        self.renderer = Renderer(self.main)
        self.menu = Menu()
        self.title = "Journal"

    def create_windows(self) -> None:
        """
        Creates the windows to pass to Renderer
        """
        h, w = self._stdscr.getmaxyx()

        #Main window
        self.main = self._stdscr.derwin(h, w, 0, 0)
        self.main.keypad(True)

    def run(self) -> None:
        """
        Main starting point for the whole thing
        """
        cont = True
        while cont:
            cont = self.main_menu()

    def draw_title(self) -> None:
        self.renderer.title(self.title)

    def draw_main_menu(self) -> None:
        self.renderer.menu_lines(self.menu.main_menu)

    def check_main_menu_ans(self) -> bool:
        """
        Might change this logic. Just get the key, then pass that key to
        some other function later
        """
        cont = True
        ans = self.renderer.get_key(8,1)
        try:
            if str(ans) not in [curses.KEY_ENTER ,10 , 13, "\n","", "l", "q"]:
                self.renderer.message_centered("Not an option..")
            if ans == curses.KEY_ENTER or ans == 10 or ans == 13 or ans == "\n":
                self.create_new_entry()
                pass
            if str(ans) == "l":
                self.list_entries()
                pass
            if str(ans) == "q":
                self.renderer.message_centered("Exiting ..")
                cont = False
        except ValueError:
            print(f"Not a string")
        return cont


    def main_menu(self) -> bool:
        cont = True
        self.renderer.clear()
        self.draw_title()
        self.draw_main_menu()
        cont = self.check_main_menu_ans()
        return cont

    def draw_new_entry(self) -> None:
        pass

    def draw_list_entries(self) -> None:
        pass

    # def write_todays_entries(self) -> None:
    #     """
    #     Checks if there have been earlier entries made today, if it has, print
    #     them to the screen and refresh
    #     """
    #     #####Issue 12:#####
    #     #if there was made an entry earlier in the day, that entry should be read
    #     #and printed to screen and we should start writing for a couple of lines down from that.
    #
    #     #First check if there are entries today:
    #     if utils.date_utils.get_today() in self.app.journalservice.list_of_entries:
    #
    #         #Then create a new object of todays entry, print it to screen and refresh
    #         # todays_entries = self.app.journalservice.new_entry(utils.date_utils.get_today())
    #         # self.renderer.prompt(1,0, self.app.journalservice.read_entry(todays_entries))
    #         # self.renderer.refresh()
    #         je = self.app.journalservice.new_entry(utils.date_utils.get_today())
    #         self.app.journalservice.read_entry(je)
    #         self.renderer.prompt(1,0, je.as_str())
    #         #self.renderer.prompt(1,0, je.as_str())
    #         self.renderer.refresh()
    #
    #     return None

    def check_if_key_is_enter(self, key: int) -> bool:
        """
        Takes a variable called key, that represents a keypress from getch().
        Check if this key is equal to several different types of values for 
        ENTER. If it is return True, if not return False.
        """
        return key in ["\n", 10, curses.KEY_ENTER]

    def check_if_key_is_backspace(self, key: int) -> bool:
        """
        Takes a variable key, that represents a keypress from getch(). Check
        if the key is equal to several different types of values for BACKSPACE.
        If it is return True, if not return False.
        """
        return key in ["ć", 263, curses.KEY_BACKSPACE]

    def go_backwards(self) -> None:
        """
        Moves the cursor one cell backwards. If at the beginning of a line it 
        jumps up one line, and starts at the end of the previous line
        """
        if self.renderer.xpos == 0 and self.renderer.ypos != 0:
            self.renderer.move(self.renderer.ypos-1, self.renderer.w-1)
        elif self.renderer.xpos != 0:
            self.renderer.move(self.renderer.ypos, self.renderer.xpos-1)
        return None

    def compare_entry_cell(self, je: journalentry.JournalEntry) -> bool:
        """
        Returns true if je.entry[-1] is equal to the content of cell under the
        cursor
        """
        cell = self.renderer.inch(self.renderer.ypos, self.renderer.xpos)
        ch = chr(cell & curses.A_CHARTEXT)
        if ch == je.entry[-1]:
            return True
        else:
            return False

    def find_last_entry(self, je: journalentry.JournalEntry) -> None:
        """
        Takes a journalentry object, and runs a loop until the the je.entry[-1]
        is equal to what is under the cursor
        """
        while True:
            if self.compare_entry_cell(je):
                break
            else:
                self.go_backwards()
        return None

    def create_new_entry(self) -> None:
        """Here we will request the inputs from the user"""
        je = self.app.journalservice.new_entry(utils.date_utils.get_today())
        self.app.journalservice.read_entry(je)
        self.renderer.clear()
        self.renderer.move(0, 0)
        self.renderer.prompt(0,0, je.as_str())
        
        while True:
            key = self.renderer.getch()
            if self.check_if_key_is_enter(key):
                je.append(key)
                break
            elif self.check_if_key_is_backspace(key):
                if (len(je.entry) == 0):
                    continue
                else:
                    # self.debug_write_and_restore("Key:" + str(key), y = self.renderer.h-5)
                    # self.debug_write_and_restore("Entry:" + str(je.entry[-1]), y = self.renderer.h-3)
                    if je.entry[-1] == " ":
                        #self.renderer.clrtoeol()
                        self.renderer.clrtobot()
                        je.pop()
                        self.go_backwards()
                    elif je.entry[-1] == "\n":
                        self.go_backwards()
                        je.pop()
                        self.renderer.clrtobot()
                        #self.renderer.clrtoeol()
                        je.pop()
                    else:
                        self.find_last_entry(je)
                        #self.renderer.clrtoeol()
                        self.renderer.clrtobot()
                        je.pop()

            else:
                #Checks if control/special characters were inputted.
                if 32 <= key <= 126 or key in (9,):
                    self.renderer.addstr(chr(key))
                    je.append(key)
                else:
                    pass

        self.app.journalservice.write_entry(je)

    def list_entries(self):
        self.renderer.clear()
        self.renderer.refresh_geometry()
        lines_available = (self.renderer.h - 3) 
        self.draw_title()

        start = 0
        entries_per_page = lines_available // 2 #Gives us two lines per entry
        total_entries = len(self.app.journalservice.list_of_entries)

        while True:
            self.renderer.clear()
            self.draw_title()
            line = 0

            #Displaying the entries from start to start + entries per parge
            for idx in range(start, min(start + entries_per_page, total_entries)):
                #sc.addstr(3 + (line*2), 1, f"{idx}) {self.app.journalservice.list_of_entries()[idx]}")
                self.renderer.prompt(3 + (line*2), 1, f"{idx}) {self.app.journalservice.list_of_entries[idx]}")
                line += 1

            curses.echo()
            self.renderer.prompt(3 + (line*2), 1, "Select entry or press Enter for next page or 'q' for main menu: ")
            self.renderer.refresh()
            #ans = sc.getstr(3 + (line*2), 65).decode("utf-8").strip()
            #TODO: remember that this might need decode
            ans = self.renderer.get_multi_key(3 + (line*2), 65)#.decode("utf-8").strip()
            curses.noecho()

            if ans == "" or ans in {"\n", "\r"}:
                start += entries_per_page
                if start >= total_entries:
                    start = 0
            else:
                try:
                    if ans == "q":
                        return 0
                    idx = int(ans)
                    if 0 <= idx < total_entries:
                        self.renderer.clear()
                        #use load_entry(filepath) from utils.py to return an entry
                        je = self.app.journalservice.new_entry(self.app.journalservice.list_of_entries[idx])
                        self.renderer.prompt(1,1, self.app.journalservice.read_entry(je))
                        self.renderer.refresh()
                        #TODO: fix this underscore
                        self.renderer.getch()
                    else:
                        self.renderer.prompt(3 + (line*2),1,"Invalid index.")
                        self.renderer.refresh()
                        #TODO: fix this udenrscore
                        self.renderer.getch()
                except ValueError:
                    self.renderer.prompt(3+(line*2),1,"Invalid input.")
                    self.renderer.refresh()
                    #TODO: fix this udenrscore
                    self.renderer.getch()
        return 0
