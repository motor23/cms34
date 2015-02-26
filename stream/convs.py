# -*- coding: utf-8 -*-
import re

from iktomi.forms.convs import ValidationError

__all__ = (
    'NoUpperConv',
    'StripTrailingDotConv',
)


def NoUpperConv(field, value):
    if value and not (value.upper()!=value or value.lower() == value):
        raise ValidationError(u'Не нужно писать БОЛЬШИМИ БУКВАМИ')
    return value


def StripTrailingDotConv(field, value):
    if value:
        value = value.rstrip('.')
    return value


