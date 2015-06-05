
import datetime as dt
import re

def parse_timestamp(raw_ts):
    date = None
    time = None
    m = re.search(r'(\d{2,4})-(\d{2})-(\d{2})', raw_ts)
    if m:
        date = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.search(r'(\d{2}):(\d{2}):(\d{2})', raw_ts)
    if m:
        time = dt.time(hour=int(m.group(1)), minute=int(m.group(2)), second=int(m.group(3)))

    return dt.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second)

