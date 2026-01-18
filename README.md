# Journal (Terminal / curses-based)

A **terminal-based journaling application** written in Python using `curses`.  
Entries are stored as plain text files (one per day) and edited directly inside a split-pane TUI.

This project is intentionally **minimal, hackable, and local-first**:
- No database
- No cloud sync
- No external dependencies beyond Python stdlib
- Human-readable files on disk 

> **Project status:** Active development / experimental.  
> Some files are incomplete, unused, or in the middle of refactors. This is expected.

---

## Features

- Terminal UI built with `curses` 
- Split-pane layout (title, main editor, status) 
- One journal entry per day (YYYY-MM-DD) 
- Create/continue today’s entry inside the terminal 
- List and open previous entries 
- Automatic config generation in `~/.config/journal/journal.conf` 
- Automatic journal directory creation (default `~/.journal`) 
- Plain-text storage (easy to back up and edit with any editor) 

---

## How it works

### Entry point

Run `journal.py`, which initializes curses and starts the UI controller loop. 

### App wiring

`App` wires together:
- `Settings` (config + defaults)
- `JournalService` (file I/O) 

### Storage model

Entries are represented by a `JournalEntry` object which stores:
- a `pathlib.Path` to the file
- an in-memory list of characters typed in the editor 

### File I/O

`JournalService`:
- ensures the journal directory exists
- lists existing entries (by filename stem)
- reads/writes entries as UTF-8 text files 

---

## Controls

Main menu (drawn from `Menu.main_menu`):

- **Enter** → create/continue today’s entry 
- **l** → list entries 
- **q** → quit 

While editing:
- Normal character keys add text to the entry 
- Backspace handling is custom (cursor movement + delete logic) 
- Enter ends the edit loop (current behavior) 

---

## Configuration

On first run, a config file is generated automatically:

Example:
```ini
# Set your preferences
save_path = ~/.journal
```

- Missing config files are generated
- Missing keys fall back to defaults
- Comments (#) are supported
- The app will not crash if the user edits the file incorrectly

Journal entries are stored as plain text files:

~/.journal/

├── 2025-02-16

├── 2025-02-17

└── 2025-02-18

Filename = date
UTF-8 encoded
Editable outside the app with any editor
Safe to back up, sync, or version-control

---

## Requirements

- Python 3.10+ recommended

- Linux / macOS terminal

- curses (included in stdlib on Unix-like systems)

- Windows is not supported without windows-curses

---

## Using a virtual environment (venv)

Even though this project currently only uses the standard library, using a venv is recommended.

### Create venv

```bash
python -m venv .venv
```

### Activate the venv
```bash
source .venv/bin/activate
```
### Upgrade pip(optional)

```bash
python -m pip install --upgrade pip
```

### Install requirements
```bash
python3 -m pip install -r requirements.txt
```

### Run the journal
```bash
python3 journal.py
```

### Deactivate venv(when done using the journal)
```bash
deactivate
```

---

## Known limitations / TODOs

- Some files are incomplete, experimental, or currently unused (e.g. `journallist.py`)
- Editor behavior is still evolving (manual cursor and backspace handling)
- No explicit terminal resize handling yet
- Minimal configuration validation
- Limited test coverage
- UI and input handling are still under active refactor

---

## Logging

The application configures basic logging at startup:

- Logs are written to both **stdout** and a local file (`script.log`)
- Logging is initialized in `journal.py`
- Intended primarily for development and debugging

---

## License

This project is licensed under the terms of the license included in the repository:

- [LICENSE](./LICENSE)

---

## Author

**Kjetil Paulsen**

- GitHub: [https://github.com/noorac](https://github.com/noorac)

---
