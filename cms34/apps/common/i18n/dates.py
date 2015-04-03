# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import babel.dates

DATE_FORMATS = {
    'ru': u"d MMMM y 'года'",
    'en': u'MMMM d, y',
}

DATETIME_FORMATS = {
    # locale: format
    'ru': u"d MMMM y 'года', HH:mm",
    'en': u'MMMM d, y, HH:mm',
}

DATETIME_FORMATS_WITHOUT_YEAR = {
    'ru': u"d MMMM, HH:mm",
    'en': u'MMMM d, HH:mm',
}

RANGE_FORMATS = {
    # locale: (start_dmy, start_dm, start_d, end)
    'ru': {
        # y1=?y2, m1=?m2, d1=?d2 : (format1, format2)
        ''   : (u'd MMMM y \N{EN DASH} ', u"d MMMM y"),
        'y'  : (u'd MMMM \N{EN DASH} ', u"d MMMM y 'года'"),
        'ym' : (u'd\N{EN DASH}', u"d MMMM y 'года'"),
        'ymd': (u"d MMMM y 'года'", u''),
    },
    'en': {
        ''   : (u'MMMM d, y \N{EN DASH} ', u'MMMM d, y'),
        'y'  : (u'MMMM d \N{EN DASH} ', u'MMMM d, y'),
        'ym' : (u'MMMM d\N{EN DASH}', u'd, y'),
        'ymd': (u'MMMM d, y', u''),
    },
}

def format_date(date, format=None, locale='en', relative=False):
    if relative:
        delta = datetime.now() - date
        if not delta.days:
            return babel.dates.format_timedelta(-delta, locale=locale, add_direction=True)
    if format is None:
        format = DATE_FORMATS[locale]
    return babel.dates.format_date(date, format, locale=locale)


def format_datetime(dt, format=None, locale='en', relative=False):
    if relative:
        delta = datetime.now() - dt
        if not delta.days:
            return babel.dates.format_timedelta(-delta, locale=locale, add_direction=True)
    if format is None:
        if dt.year == datetime.now().year:
            format = DATETIME_FORMATS_WITHOUT_YEAR[locale]
        else:
            format = DATETIME_FORMATS[locale]
    return babel.dates.format_datetime(dt, format, locale=locale)


def format_daterange(start, end, locale='en'):
    if end is None:
        end = start
    key = ''
    for attr in ['year', 'month', 'day']:
        if getattr(start, attr)!=getattr(end, attr):
            break
        key += attr[0]
    start_format, end_format = RANGE_FORMATS[locale][key]
    return babel.dates.format_date(start, start_format, locale=locale) + \
            babel.dates.format_date(end, end_format, locale=locale)
