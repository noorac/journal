#app: wires services + ui (no curses logic)


from services import journalservice

class App:
    """
    A starting point
    """
    def __init__(self) -> None:
        self.journalservice = journalservice.JournalService

