# -*- coding: utf-8 -*-
from iktomi.utils import quote_js
from iktomi.utils.text import pare
from datetime import datetime, date, timedelta


__all__ = (
    'ru_strftime',
    'en_strftime',
    'get_plural',
    'quote_js',
    'pare',
    'ru_float_format',
    'ru_int_format',
    'smart_ru_strftime',
)

def strftime(date, format, lang="ru", inflected=False):
    if lang == 'ru':
        return ru_strftime(date, format, inflected)
    else:
        return date.strftime(format)


def ru_strftime(date, format, inflected=False):
    return dt.ru_strftime(unicode(format), date, inflected)


def en_strftime(date, format):
    format = format.encode('utf-8')
    # XXX Dirty hack, this won't work in some cases
    format = format.replace('%d', str(date.day))
    # XXX This works when locale is not set only
    return date.strftime(format).decode('utf-8')


def ru_int_format(num):
    int_ = str(num)
    if len(int_) > 4:
        i = len(int_)
        while i>0:
            int_ = int_[0:i] + ' ' + int_[i:]
            i -= 3
    return int_

def ru_float_format(num, fmt):
    s = fmt % num
    if '.' in s:
        int_, flo_ = s.split('.')
        return ru_int_format(int_) + ',' + flo_
    return ru_int_format(s)

def smart_ru_strftime(start, end=None, year=True, force_year=False,
                      today=True, yesterday=True,
                      d=None, m=None, y=u'%Y г.'):
    '''Datetime for strana'''
    if start is None:
        return u'Дата и время не заданы'
    today_ = date.today()
    if isinstance(start, datetime):
        start = start.date()
    if isinstance(end, datetime):
        end = end.date()


    def _fmt(format_, date):
        if d: format_ = format_.replace('%d', d)
        if m: format_ = format_.replace('%B', m)
        if y: format_ = format_.replace('%Y', y)
        return dt.ru_strftime(format_, date, inflected=True)

    if end is None or end == start:
        if today and start == today_:
            return u'Сегодня'
        if yesterday and start + timedelta(1) == today_:
            return u'Вчера'
        if (not force_year and \
            (not year or start.year == today_.year)):
            return _fmt(u'%d %B', start)
        return _fmt(u'%d %B %Y', start)
    else:
        join_template = u"%s — %s"
        if start.year == end.year and start.month == end.month:
            start_str = str(start.day)
            join_template = u"%s—%s"
        elif start.year == end.year:
            start_str = _fmt(u'%d %B', start)
        else:
            start_str = _fmt(u'%d %B %Y', start)
        if start + timedelta(1) == end:
            join_template = u"%s, %s"
        if (not force_year and
             (not year or start.year == today_.year \
                       and end.year == today_.year)):
            end_str = _fmt(u'%d %B', end)
        else:
            end_str = _fmt(u'%d %B %Y', end)
        return join_template % (start_str, end_str)

all_functions = dict((k,v) for k, v in locals().items() if k in __all__)
