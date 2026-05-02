from datetime import datetime
from argparse import ArgumentParser, Namespace
import os
import sys
from zoneinfo import ZoneInfo
import re
from datetime import timedelta
from typing import TextIO



from ..guess import guess_format
from ..vprint import vprint, set_verbose



def parse_duration(s: str) -> timedelta:
    units = {
        's': 'seconds',
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks',
    }
    
    # просто число — считаем секундами
    if s.isdigit():
        return timedelta(seconds=int(s))
    
    matches = re.findall(r'(\d+)([smhdw])', s)
    if not matches:
        raise ValueError(f"Cannot parse duration: {s!r}")
    
    kwargs = {}
    for value, unit in matches:
        kwargs[units[unit]] = int(value)
    
    return timedelta(**kwargs)

def get_args() -> Namespace:
    parser = ArgumentParser('grepago - grep log files by date in any format')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='verbose mode')
    parser.add_argument('-p', '--prepend', default=False, action='store_true', help='prepend each output line with human-readable time e.g. 2026/04/28 13:37:34')
    parser.add_argument('duration', type=str, help='Duration (how much time ago from now, e.g. 1h or 1h30m or 3d)')
    parser.add_argument('FILES', nargs='*')
    
    return parser.parse_args()

def mytz():
    mytz = os.readlink('/etc/localtime').split('zoneinfo/')[-1]
    return ZoneInfo(mytz)


def main():
    args = get_args()
    set_verbose(args.verbose)    

    duration = parse_duration(args.duration)
    cutoff = datetime.now(tz=mytz()) - duration
    vprint(f"# Duration: {duration} cutoff: {cutoff} tz: {cutoff.tzinfo}")

    if args.FILES:
        for fname in args.FILES:
            filesize = os.path.getsize(fname)
            if filesize == 0:
                vprint(f'# skip empty file {fname}')
                continue

            vprint(f'# process file {fname} ({filesize} bytes)')
            with open(fname) as fh:
                grep_file(fh=fh, cutoff=cutoff, prepend=args.prepend)
    else:
        grep_file(sys.stdin, cutoff=cutoff, prepend=args.prepend)

def grep_file(fh: TextIO, cutoff: datetime, prepend: bool = False):
    l1 = fh.readline()
    
    # print(l1)
    fcls, dt = guess_format(l1)
    vprint(f'# detected format {fcls}')
    fh.seek(0)

    for idx,line in enumerate(fh):
        line = line.rstrip()
        try:
            dt = fcls.get_datetime(line)
            if dt >= cutoff:
                # print it!
                if prepend:
                    print(dt.strftime('%Y/%m/%d %H:%M:%S'), line)
                else:
                    print(line)
        except ValueError:
            vprint(f'# Cannot parse line {idx}: {line}')


if __name__ == '__main__':
    main()

