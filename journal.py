#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: journal.py
Description: Main program for journal
Author: Kjetil Paulsen
Date: 2025-02-17
"""
#making a change
#and another
# =========================
# Imports
# =========================
import time
import curses
import logging
import os
import sys
import datetime

import utils.utils
import utils.date_utils
import model.journalentry

# =========================
# Constants
# =========================
VERSION = "1.0.0"
LOG_FILE = "script.log"

# =========================
# Logger Configuration
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


# =========================
# Helper Functions
# =========================


def title_message(h,w,string):
    sc.clear()
    sc.addstr(h-h+1, w//2-len(string)//2,string)
    sc.refresh()
    time.sleep(0.75)
    return None

def startup_curses():
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_RED)
    return None

def draw_title():
    height,width = sc.getmaxyx()
    title = "Journal"
    sc.addstr(height-height+1,width//2-len(title)//2,title,curses.color_pair(1))
    return None

def draw_menu():
    height, width = sc.getmaxyx()
    opt1 = "E) Press enter for new entry"
    opt2 = "l) Press l for list"
    opt3 = "q) press q to quit"
    sc.addstr(height-height+3, width-width+1, opt1)
    sc.addstr(height-height+4, width-width+1, opt2)
    sc.addstr(height-height+5, width-width+1, opt3)
    return None


def get_filenames(directory):
    """Returns a list of filenames in the given directory."""
    return [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]


def load_journals():
    return 0
#This has been tampered with.
def create_entry():
    sc.clear()
    draw_title()
    sc.refresh()
    curses.echo()
    sc.move(2,1)
    #JournalEntry.write_entry(sc) goes here
    curses.noecho()
    return None

# class journal_entry:
#     def __init__(self, filename) -> None:
#         self.filename = filename
#         self.filepath = "/home/noorac/.journal/" + self.filename
#         return None
#
#     def new_entry(self):
#         self.entry_list = create_entry()
#         self.entry = ""
#         for i in range(len(self.entry_list)):
#             self.entry += self.entry_list[i]
#         self.entry = self.entry + "\n\n"
#         self.f = open(self.filepath, "a")
#         self.f.write(self.entry)
#         self.f.close()
#         return None
#
#     def load_entry(self):
#         self.f = open(self.filepath, "r")
#         for x in self.f:
#             sc.addstr(x)
#         self.f.close()


#This is a menu option. Looking into refactors.

def new_entry(journal_dict):
    today = utils.date_utils.get_today()
    if today in journal_dict:
        journal_dict[today].new_entry()
    else:
        journal_dict[today] = model.journalentry.JournalEntry(today) #journal_entry(today)
        journal_dict[today].new_entry()
    return 0

# THis is a menu option, and should be significantly refactored. It lists the
# entries, and if we chose an entry, it can then be shown to the screen.
def list_entries(journal_dict):
    sc.clear()
    h, w = sc.getmaxyx()
    lines_available = (h - 3) 
    draw_title()

    start = 0
    entries_per_page = lines_available // 2 #Gives us two lines per entry
    total_entries = len(journal_dict)

    while True:
        sc.clear()
        draw_title()
        line = 0

        #Displaying the entries from start to start + entries per parge
        for idx in range(start, min(start + entries_per_page, total_entries)):
            sc.addstr(3 + (line*2), 1, f"{idx}) {list(journal_dict.keys())[idx]}")
            line += 1

        curses.echo()
        sc.addstr(3 + (line*2), 1, "Select entry or press Enter for next page or 'q' for main menu: ")
        sc.refresh()
        ans = sc.getstr(3 + (line*2), 65).decode("utf-8").strip()
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
                    sc.clear()
                    #use load_entry(filepath) from utils.py to return an entry
                    sc.addstr(lines_available,1, str(journal_dict[list(journal_dict.keys())[idx]].load_entry()))
                    sc.refresh()
                    sc.getch()
                else:
                    sc.addstr(3 + (line*2),1,"Invalid index.")
                    sc.refresh()
                    sc.getch()
            except ValueError:
                sc.addstr(3+(line*2),1,"Invalid input.")
                sc.refresh()
                sc.getch()
    return 0



# Turn into dict? is this neccecary? Or should it be done here. It takes a 
#list of filenames im assuming, and then builds the dict of all objects. I 
# guess it is neccecary for now.

def turn_dict(journal_list) -> dict:
    journal_dict = {}
    if len(journal_list) > 0:
        for i in range(len(journal_list)):
            journal_dict[journal_list[i]] = model.journalentry.JournalEntry(journal_list[i]) #journal_entry(journal_list[i])
    return journal_dict

#Menus should be rewritten in a separate menu-class?

def menu(journal_dict) -> bool:
    #clear_screen()
    journal_dict = journal_dict
    cont = True
    height,width = sc.getmaxyx()
    sc.clear()
    draw_title()
    draw_menu()
    sc.refresh()
    ans = sc.getkey(8,1)
    sc.refresh()
    try:
        if str(ans) not in [curses.KEY_ENTER ,10 , 13, "\n","", "l", "q"]:
            title_message(height,width,"Not an option..")
        if ans == curses.KEY_ENTER or ans == 10 or ans == 13 or ans == "\n":
            new_entry(journal_dict)
        if str(ans) == "l":
            list_entries(journal_dict)
        if str(ans) == "q":
            title_message(height,width,"Exiting ..")
            cont = False
    except ValueError:
        print(f"Not a string")
    return cont


# =========================
# Main Function
# =========================
def main(stdscr):
    """
    Main function to run the script.
    """
    logger.info("Starting journal.py ..")
    time.sleep(0.5)
    global sc
    sc = stdscr
    startup_curses()
    filepath = "/home/noorac/.journal"
    journal_list = get_filenames(filepath)
    journal_list.sort()
    journal_dict = turn_dict(journal_list)
    cont = True
    while cont:
        cont = menu(journal_dict)


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        logger.warning("Script interrupted by the user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)
