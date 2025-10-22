#uicontroller: event loop, screens, focus, routes keys
import curses
from models.journalentry import JournalEntry
from ui.menu.menu import Menu
from ui.curses.renderer import Renderer
import utils.date_utils

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


    def create_new_entry(self) -> None:
        """Here we will request the inputs from the user"""
        entry_list = []
        key = -1
        self.renderer.clear()
        self.renderer.refresh()
        self.renderer._stdscr.move(2, 0)
        curses.echo()


        #Here is a bunch of mess because of different terminals call enter and 
        #backspace different things. So need to cover bases. Essentially if 
        #enter is pressed, the loop is ended and entry saved, if backspace is 
        #pressed, it backspaces.
        while not ( key == curses.KEY_ENTER or key == 10 or key == 13 or key == "\n"):
            key = self.renderer._stdscr.getch()
            if key in ["ć", curses.KEY_BACKSPACE]:
                self.renderer.refresh_geometry()
                h, w = self.renderer._stdscr.getyx()
                if w == 0 and (not (h == 2)):
                    self.renderer._stdscr.move(h-1, self.renderer.w-1)
                self.renderer._stdscr.delch()
                if (len(entry_list) > 0):
                    entry_list.pop(-1)
            else:
                entry_list.append(chr(key))

        curses.noecho()
        je = self.app.journalservice.new_entry(utils.date_utils.get_today())
        self.app.journalservice.write_entry(je, "".join(entry_list))

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
                        self.renderer._stdscr.getch()
                    else:
                        self.renderer.prompt(3 + (line*2),1,"Invalid index.")
                        self.renderer.refresh()
                        #TODO: fix this udenrscore
                        self.renderer._stdscr.getch()
                except ValueError:
                    self.renderer.prompt(3+(line*2),1,"Invalid input.")
                    self.renderer.refresh()
                    #TODO: fix this udenrscore
                    self.renderer._stdscr.getch()
        return 0
