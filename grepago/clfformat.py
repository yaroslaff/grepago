from datetime import datetime
import re

from .logformat import LogFormat


class CLFFormat(LogFormat):
    """ Common/Combined Log Format (nginx/apache) """

    pattern = r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s[+-]\d{4})\]'


    def get_datetime(self, line: str) -> datetime:
        m = re.search(self.pattern, line)
        if m:
            dt = datetime.strptime("29/Apr/2026:07:38:19 +0200", "%d/%b/%Y:%H:%M:%S %z")
            return dt
        
        return ValueError(f'Not a CLF format: {line.rstrip()}')
    
