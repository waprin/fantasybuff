import datetime

__author__ = 'bprin'


def real_num_weeks():
    start = datetime.datetime(year=2014, month=9, day=9)
    week = datetime.timedelta(days=7)
    start_days = [start + (weeknum * week) for weeknum in range(0, 17)]
    now = datetime.datetime.now()
    for i in range(0, 17):
        if now < start_days[i]:
            return i
    return 17
