import datetime

def get_today() -> str:
    """Returns the current date on the format YYYY-MM-DD"""
    return datetime.datetime.now().strftime("%Y-%m-%d")
