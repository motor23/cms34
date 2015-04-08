# -*- coding: utf-8 -*-

from iktomi.utils import cached_property, weakproxy
from babel import Locale
from babel.support import Format
from babel.dates import format_time, format_timedelta
from .dates import format_date, format_datetime, format_daterange
from .translation import get_translations
from jinja2 import Markup
from pytz import timezone


class delegate_cached(property):

    def __init__(self, to, what):
        self._to = to
        self._what = what

    def __get__(self, inst, cls=None):
        if inst is None:
            return self
        result = getattr(getattr(inst, self._to), self._what)
        inst.__dict__[self._what] = result
        return result


class Lang(str):

    def __new__(cls, name, root, translations_dir, categories=[]):
        self = str.__new__(cls, name)
        self.format = Format(name)
        self.timezone = timezone('Europe/Moscow')
        self.root = getattr(root, name)
        self._translations = get_translations(translations_dir, self, categories)
        return self

    @cached_property
    def url_for(self):
        return self.root.build_url

    def months(self, **kwargs):
        type = kwargs.get('type', 'stand-alone')
        form = kwargs.get('form', 'wide')
        locale = Locale(self)
        return locale.months[type][form]

    def gettext(self, msgid):
        message = self._translations.gettext(unicode(msgid))
        if isinstance(msgid, Markup):
            message = Markup(message)
        return message

    def ngettext(self, msgid1, msgid2, n):
        message = self._translations.ngettext(unicode(msgid1),
                                              unicode(msgid2), n)
        if isinstance(msgid1, Markup):
            message = Markup(message)
        return message

    def _(self, msgid):
        return self.gettext(msgid)

    def date(self, date, format=None, relative=False):
        return format_date(date, format, locale=self, relative=relative)

    def datetime(self, datetime, format=None, relative=False):
        return format_datetime(datetime, format, locale=self, relative=relative)

    def daterange(self, start, end):
        return format_daterange(start, end, locale=self)

    def other_version(self, obj):
        if hasattr(obj, '_item_version') and self.other:
            return obj._item_version('front', self.other)

    def isodate(self, value):
        return self.timezone.localize(value).isoformat()


# date and datetime are reimplemented to use project-specific default formats
for name in ['currency', 'decimal', 'number', 'percent', 'scientific',
             'time', 'timedelta']:
    setattr(Lang, name, delegate_cached('format', name)) 
