#uicontroller: event loop, screens, focus, routes keys
import curses
import time
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
        self.title_w = Renderer(self.title)
        self.main_w = Renderer(self.main)
        self.status_w = Renderer(self.status)
        self.menu = Menu()
        self.title_text = "Journal"

    def create_windows(self) -> None:
        """
        Creates the windows to pass to renderer
        """
        #Get amount we have to play with
        h, w = self._stdscr.getmaxyx()
        #set frame sizes
        title_frame_h = 4
        title_frame_w = w

        main_frame_h = h - 10
        main_frame_w = w

        status_frame_h = 6
        status_frame_w = w

        #Create frames
        self.title_frame = self._stdscr.derwin(title_frame_h, title_frame_w, 0, 0)
        self.main_frame = self._stdscr.derwin(main_frame_h, main_frame_w, h - main_frame_h - status_frame_h, 0)
        self.status_frame = self._stdscr.derwin(status_frame_h, status_frame_w, h - status_frame_h, 0)

        #Create inner windows
        self.title = self.title_frame.derwin(title_frame_h - 2, title_frame_w - 2, 1, 1)
        self.main = self.main_frame.derwin(main_frame_h - 2, main_frame_w - 2, 1, 1)
        self.status = self.status_frame.derwin(status_frame_h - 2, status_frame_w - 2, 1, 1)
        
        #Set keypads
        self.title.keypad(True)
        self.main.keypad(True)
        self.status.keypad(True)

        #Set borders
        #cosider this in renderer later
        self.title_frame.box()
        self.main_frame.box()
        self.status_frame.box()

        self.title_frame.noutrefresh()
        self.main_frame.noutrefresh()
        self.status_frame.noutrefresh()
        curses.doupdate()

        return None

    def run(self) -> None:
        """
        Main starting point for the whole thing
        """
        cont = True
        while cont:
            cont = self.main_menu()

    def draw_title(self) -> None:
        #self.title_w.title(self.title_text)
        attr = curses.color_pair(1) | curses.A_UNDERLINE | curses.A_BOLD
        self.title_w.message_centered(self.title_text, attr = attr)

    def draw_main_menu(self) -> None:
        self.main_w.menu_lines(self.menu.main_menu)

    def check_main_menu_ans(self) -> bool:
        """
        Might change this logic. Just get the key, then pass that key to
        some other function later
        """
        cont = True
        ans = self.main_w.getkey(8,1)
        try:
            if str(ans) not in [curses.KEY_ENTER ,10 , 13, "\n","", "l", "q"]:
                self.main_w.message_centered("Not an option..")
            if ans == curses.KEY_ENTER or ans == 10 or ans == 13 or ans == "\n":
                self.create_new_entry()
                pass
            if str(ans) == "l":
                self.list_entries()
                pass
            if str(ans) == "q":
                self.main_w.message_centered("Exiting ..", y = 2)
                time.sleep(750/1000)
                cont = False
        except ValueError:
            print(f"Not a string")
        return cont


    def main_menu(self) -> bool:
        cont = True
        self.main_w.clear()
        self.draw_title()
        self.draw_main_menu()
        cont = self.check_main_menu_ans()
        return cont

    def draw_new_entry(self) -> None:
        pass

    def draw_list_entries(self) -> None:
        pass

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
        return key in ["ć", 263, curses.KEY_BACKSPACE, "KEY_BACKSPACE"]

    def go_backwards(self) -> None:
        """
        Moves the cursor one cell backwards. If at the beginning of a line it 
        jumps up one line, and starts at the end of the previous line
        """
        if self.main_w.xpos == 0 and self.main_w.ypos != 0:
            self.main_w.move(self.main_w.ypos-1, self.main_w.max_w-1)
        elif self.main_w.xpos != 0:
            self.main_w.move(self.main_w.ypos, self.main_w.xpos-1)
        return None

    def compare_entry_cell(self, je: journalentry.JournalEntry) -> bool:
        """
        Returns true if je.entry[-1] is equal to the content of cell under the
        cursor
        """
        cell = self.main_w.inch(self.main_w.ypos, self.main_w.xpos)
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
        self.main_w.clear()
        self.main_w.move(0, 0)
        self.main_w.addstr(0,0, je.as_str())
        
        while True:
            curses.curs_set(1)
            key = self.main_w.getkey()
            curses.curs_set(0)
            if self.check_if_key_is_enter(key):
                je.append(key)
                break
            elif self.check_if_key_is_backspace(key):
                if (len(je.entry) == 0):
                    continue
                else:
                    if je.entry[-1] == " ":
                        #self.main_w.clrtoeol()
                        self.main_w.clrtobot()
                        je.pop()
                        self.go_backwards()
                    elif je.entry[-1] == "\n":
                        self.go_backwards()
                        je.pop()
                        self.main_w.clrtobot()
                        #self.main_w.clrtoeol()
                        je.pop()
                    else:
                        self.find_last_entry(je)
                        #self.main_w.clrtoeol()
                        self.main_w.clrtobot()
                        je.pop()

            else:
                if len(key) == 1:
                    self.main_w.addstr(key)
                    je.append(key)

        self.app.journalservice.write_entry(je)

    def get_list_ans(self, line: int) -> str:
        """
        Asks the user for an input to decide which entry to show.
        """
        curses.echo()
        self.main_w.addstr(3 + (line*2), 1, "Select entry or press Enter for next page or 'q' for main menu: ")
        self.main_w.refresh()
        ans = self.main_w.get_multi_key(3 + (line*2), 65)#.decode("utf-8").strip()
        curses.noecho()
        return ans

    def list_entries(self):
        self.main_w.clear()
        self.main_w.refresh_geometry()
        lines_available = (self.main_w.max_h - 3) 
        self.draw_title()

        start = 0
        entries_per_page = lines_available // 2 #Gives us two lines per entry
        total_entries = len(self.app.journalservice.list_of_entries)

        while True:
            self.main_w.clear()
            self.draw_title()
            line = 0

            #Displaying the entries from start to start + entries per parge
            for idx in range(start, min(start + entries_per_page, total_entries)):
                self.main_w.addstr(3 + (line*2), 1, f"{idx}) {self.app.journalservice.list_of_entries[idx]}")
                line += 1

            #get line from user
            ans = self.get_list_ans(line)

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
                        self.main_w.clear()
                        #use load_entry(filepath) from utils.py to return an entry

                        je = self.app.journalservice.new_entry(self.app.journalservice.list_of_entries[idx])
                        self.app.journalservice.read_entry(je)
                        self.main_w.addstr(0,0, je.as_str())
                        self.main_w.refresh()
                        self.main_w.getch()
                    else:
                        self.main_w.addstr(3 + (line*2),1,"Invalid index.")
                        self.main_w.refresh()
                        self.main_w.getch()
                except ValueError:
                    self.main_w.addstr(3+(line*2),1,"Invalid input.")
                    self.main_w.refresh()
                    self.main_w.getch()
        return 0
