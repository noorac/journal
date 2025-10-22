#app: wires services + ui (no curses logic)


from services import journalservice

class App:
    """
    A starting point
    """
    def __init__(self, journaldirectory) -> None:
        self.journalservice = journalservice.JournalService(journaldirectory)

