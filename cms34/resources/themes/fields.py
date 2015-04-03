# -*- coding: utf8 -*-

from ...mixed import (
    XF_StreamSelect,
)

class XF_Themes(XF_StreamSelect):
    name = 'themes'
    label = u'Темы'
    model = 'Theme'
    stream_name = 'themes'
    multiple = True


xf_themes = XF_Themes()

