import datetime

import logging
import pytz

logger = logging.getLogger(__name__)
__author__ = 'bprin'

from django.utils.timezone import  is_aware, make_aware

def num_weeks_before_date(date):
    start = datetime.datetime(year=2014, month=9, day=9)
    week = datetime.timedelta(days=7)
    max_week = 15
    start_days = [start + (weeknum * week) for weeknum in range(0, max_week)]
    start_days = map(lambda day: make_aware(day, timezone=pytz.utc), start_days)
    if not is_aware(date):
        date = make_aware(date, pytz.utc)

    logger.debug("is aware %s %s" % (str(is_aware(date)), str(is_aware(start_days[0])) ))
    for i in range(0, max_week):
        if date < start_days[i]:
            return i
    return max_week

def real_num_weeks():
    return num_weeks_before_date(datetime.datetime.now())

