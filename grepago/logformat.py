from datetime import datetime

class LogFormat:
    def __init__(self):
        pass

    def get_datetime(self, line: str) -> datetime:
        pass

    def __repr__(self):
        return self.__class__.__name__
