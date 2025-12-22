#app: wires services + ui (no curses logic)


from config import settings
from services import journalservice

class App:
    """
    A starting point
    """
    def __init__(self, journaldirectory) -> None:
        self.settings = settings.Settings()
        self.journalservice = journalservice.JournalService(self.settings.savepath)

