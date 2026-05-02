from datetime import datetime
import re

from .logformat import LogFormat


class CLFFormat(LogFormat):
    """ Common/Combined Log Format (nginx/apache) """
    """
        11.22.33.44 - - [02/May/2026:06:17:41 +0200] "POST /x/webhook HTTP/1.1" 404 120 "-" "docusign"
    """

    pattern = r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s[+-]\d{4})\]'

    def get_datetime(self, line: str) -> datetime:
        m = re.search(self.pattern, line)
        if m:
            dt = datetime.strptime(m.group(1), "%d/%b/%Y:%H:%M:%S %z")
            return dt
        
        return ValueError(f'Not a CLF format: {line.rstrip()}')
    
