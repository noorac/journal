#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: journal.py
Description: Main program for journal
Author: Kjetil Paulsen
Date: 2025-02-17
"""

# =========================
# Imports
# =========================
import os
import sys
import logging

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
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# =========================
# Helper Functions
# =========================
def clear_screen() -> None:
    """
    Clears the terminal
    """
    os.system("cls" if os.name == "nt" else "clear")
    return None

def get_filenames(directory):
    """Returns a list of filenames in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def load_journals() :
    return 0


class journal_entry :
    def __init__(self, filename) -> None:
        self.filename = filename
        self.filepath = "/home/noorac/.journal/"+self.filename
        return None
    def new_entry(self):
        self.entry = input("Whats your entry: \n")
        self.entry = self.entry + "\n\n"
        self.f = open(self.filepath, "a")
        self.f.write(self.entry)
        self.f.close()
        return None

    def load_entry(self):
        self.f = open(self.filepath, "r")
        for x in self.f:
            print(x)
        #print(self.f.read())
        self.f.close()

def new_entry(journal_dict) :
    import datetime
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    if today in journal_dict:
        journal_dict[today].new_entry()
    else:
        journal_dict[today] = journal_entry(today)
        journal_dict[today].new_entry()
    return 0

def list_entries(journal_dict) :
    journal_dict = journal_dict
    clear_screen()
    for i in range(len(journal_dict)):
        print(f"{i}) {list(journal_dict.keys())[i]}\n")
    choise = input("Which you wanna cat?")
    print(list(journal_dict.values())[int(choise)].load_entry())
    wait = input("\nWaiting...")
    
    return 0

def turn_dict (journal_list) -> dict:
    journal_dict = {}
    if len(journal_list) > 0:
        for i in range(len(journal_list)):
            journal_dict[journal_list[i]] = journal_entry(journal_list[i])
    return journal_dict

def menu (journal_dict) -> bool :
    clear_screen()
    journal_dict = journal_dict
    cont = True
    print(f"Journal\n\n")
    print(f"1) Press enter for new entry\n")
    print(f"2) Press l for list of current entries\n\n")
    print(f"q) Press q to quit\n\n")
    ans = input(f"Option: ")
    try:
        if ans not in ["","l","q"]:
            print(f"Not an option")
        if ans == "":
            new_entry(journal_dict)
        if ans == "l":
            list_entries(journal_dict)
        if ans == "q":
            cont = False
    except ValueError:
        print(f"Not a string")
    return cont

# =========================
# Main Function
# =========================
def main():
    """
    Main function to run the script.
    """
    logger.info("Starting journal.py ..")
    filepath = "/home/noorac/.journal"
    journal_list = get_filenames(filepath)
    journal_dict = turn_dict(journal_list)
    cont = True
    while cont:
        cont = menu(journal_dict)

# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Script interrupted by the user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)
