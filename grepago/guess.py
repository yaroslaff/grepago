from .logformat import LogFormat
from .isoformat import ISOFormat
from .clfformat import CLFFormat

from datetime import datetime



format_classes: list[LogFormat] = [ ISOFormat(), CLFFormat() ]

def guess_format(line) -> tuple[LogFormat, datetime]:
    for fmt in format_classes:
        try:
            dt = fmt.get_datetime(line)
        except ValueError as e:
            pass
        else:
            print(f"fmt: {fmt}, dt: {dt}")
            return fmt, dt
        