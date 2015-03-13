# -*- coding: utf8 -*-

from ...mixed import (
    XF_StreamSelect,
)

class XF_Selections(XF_StreamSelect):
    name = 'selectiona'
    label = u'Выборки'
    model = 'Selection'
    stream_name = 'selections'
    multiple = True


xf_selections = XF_Selections()

