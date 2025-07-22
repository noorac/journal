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

def create_entry():
    sc.clear()
    draw_title()
    sc.refresh()
    key = -1
    curses.echo()
    sc.move(2,1)
    entry = []
    #Here is a bunch of mess because of different terminals call enter and 
    #backspace different things. So need to cover bases.
    while not ( key == curses.KEY_ENTER or key == 10 or key == 13 or key == "\n"):
        key = sc.getch()
        if key in ["ć", curses.KEY_BACKSPACE]:
            sc.delch()
            entry.pop(-1)
        else:
            entry.append(chr(key))
    curses.noecho()
    return entry

class journal_entry:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.filepath = "/home/noorac/.journal/" + self.filename
        return None

    def new_entry(self):
        self.entry_list = create_entry()
        self.entry = ""
        for i in range(len(self.entry_list)):
            self.entry += self.entry_list[i]
        self.entry = self.entry + "\n\n"
        self.f = open(self.filepath, "a")
        self.f.write(self.entry)
        self.f.close()
        return None

    def load_entry(self):
        self.f = open(self.filepath, "r")
        for x in self.f:
            sc.addstr(x)
        self.f.close()


def new_entry(journal_dict):
    import datetime

    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    if today in journal_dict:
        journal_dict[today].new_entry()
    else:
        journal_dict[today] = journal_entry(today)
        journal_dict[today].new_entry()
    return 0


def list_entries(journal_dict):
    sc.clear()
    h, w = sc.getmaxyx()
    lines_available = (h - 3) 
    draw_title()
    wherearewe = 0
    for i in range(len(journal_dict)):
        if wherearewe < lines_available:
            sc.addstr(h-h+3+(i*2),w-w+1,f"{i}) {list(journal_dict.keys())[i]}")
            print(f"{i}) {list(journal_dict.keys())[i]}\n")
            wherearewe = 3 + i*2 + 2
    curses.echo()
    ans = sc.getstr(wherearewe,1).decode("utf-8")
    curses.noecho()
    #if ans == curses.KEY_ENTER or ans == 10 or ans == 13 or ans == "\n":
    sc.clear()
    sc.addstr(str(list(journal_dict.values())[int(ans)].load_entry()))
    sc.refresh()
    sc.getch()
    #wait = input("\nWaiting...")

    return 0


def turn_dict(journal_list) -> dict:
    journal_dict = {}
    if len(journal_list) > 0:
        for i in range(len(journal_list)):
            journal_dict[journal_list[i]] = journal_entry(journal_list[i])
    return journal_dict


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
