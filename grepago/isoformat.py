from datetime import datetime

from .logformat import LogFormat

class ISOFormat(LogFormat):

    def get_datetime(self, line: str) -> datetime:
        dateline = line.split(' ')[0]
        return datetime.fromisoformat(dateline)
    
